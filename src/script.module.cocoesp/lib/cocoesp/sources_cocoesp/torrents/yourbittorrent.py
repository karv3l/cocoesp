# -*- coding: utf-8 -*-
"""
	cocoesp - YourBittorrent (multi-idioma, con búsqueda adicional «spa»). Spec 007.
	Usa el RSS público de búsqueda (https://yourbittorrent.com/rss.xml?q=...): la web HTML
	está tras un desafío de Cloudflare que NO se intenta resolver.
	El RSS no trae el infohash: se descarga el .torrent del <enclosure> y se calcula.
"""
import re
from html import unescape
from urllib.parse import quote_plus
from cocoesp.modules import coco_client as client, coco_compat as source_utils
from cocoesp.modules.spanish_sites import torrent_info, is_archive_only

_ITEM_RE = re.compile(r'<item>(.*?)</item>', re.S)
_TITLE_RE = re.compile(r'<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>', re.S)
_ENCLOSURE_RE = re.compile(r'<enclosure\s+url=["\']([^"\']+)["\']', re.I)
_SEEDS_RE = re.compile(r'Seeds:\s*(\d+)', re.I)
_SIZE_RE = re.compile(r'Size:\s*([\d.,]+\s*[KMGT]i?B)', re.I)


def parse_rss(xml):
	"""[{'title','torrent','seeders','size'}] de un RSS de YourBittorrent."""
	items = []
	for block in _ITEM_RE.findall(xml or ''):
		t, e = _TITLE_RE.search(block), _ENCLOSURE_RE.search(block)
		if not t or not e: continue
		s, z = _SEEDS_RE.search(block), _SIZE_RE.search(block)
		items.append({'title': unescape(t.group(1)).strip(), 'torrent': unescape(e.group(1)),
					  'seeders': int(s.group(1)) if s else 0, 'size': z.group(1) if z else ''})
	return items


class source:
	timeout = 10
	priority = 3
	pack_capable = False
	hasMovies = True
	hasEpisodes = True
	MAX_TORRENTS = 10

	def __init__(self):
		self.language = ['en', 'es']
		self.base_link = 'https://yourbittorrent.com'
		self.search_link = '/rss.xml?q=%s'
		self.min_seeders = 0

	def _get(self, url, binary=False):
		try:
			r = client.session.request('get', url, headers={'User-Agent': client.randomagent()}, timeout=self.timeout)
			if r.status_code != 200: return None
			return r.content if binary else r.text
		except Exception:
			return None

	def _queries(self, title, hdlr, es_aliases, lang_mode):
		queries = ['%s %s' % (title, hdlr)]
		if lang_mode in (source_utils.LANG_SPANISH, source_utils.LANG_MULTI):
			queries.append('%s %s spa' % (title, hdlr) if hdlr.startswith('S') else '%s spa' % title)
			queries.extend('%s %s' % (a, hdlr) for a in es_aliases[:1])
		out = []
		for q in queries:
			q = re.sub(r'\s+', ' ', q).strip()
			if q.lower() not in [x.lower() for x in out]: out.append(q)
		return out[:3]

	def sources(self, data, hostDict):
		sources = []
		if not data: return sources
		try:
			airdate = source_utils.episode_airdate(data) if 'tvshowtitle' in data else None
			aliases = source_utils.aliases_to_array(data['aliases'])
			es_aliases = [a for a in source_utils.aliases_to_array(data['aliases'], ['es']) if a]
			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			title = title.replace('&', 'and').replace('/', ' ').replace('$', 's')
			episode_title = data['title'] if 'tvshowtitle' in data else None
			year = data['year']
			if 'tvshowtitle' in data:
				hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])); years = None
			else:
				hdlr = year; years = [str(int(year) - 1), str(year), str(int(year) + 1)]
			if 'timeout' in data: self.timeout = int(data['timeout'])
			undesirables = source_utils.get_undesirables()
			check_foreign_audio = source_utils.check_foreign_audio()
			queries = self._queries(title, hdlr, es_aliases, source_utils.language_mode())
		except Exception:
			source_utils.scraper_error('YOURBITTORRENT')
			return sources

		candidates, seen_titles = [], set()
		for q in queries:
			for item in parse_rss(self._get(self.base_link + self.search_link % quote_plus(q))):
				if item['title'] in seen_titles: continue
				seen_titles.add(item['title'])
				try:
					name = source_utils.clean_name(item['title'])
					if not source_utils.check_title(title, aliases, name, hdlr, year, years, airdate=airdate): continue
					name_info = source_utils.info_from_name(name, title, year, hdlr, episode_title, airdate=airdate)
					if source_utils.remove_lang(name_info, check_foreign_audio): continue
					if undesirables and source_utils.remove_undesirables(name_info, undesirables): continue
					if self.min_seeders > item['seeders']: continue
					candidates.append((item, name, name_info))
				except Exception:
					source_utils.scraper_error('YOURBITTORRENT')

		candidates.sort(key=lambda c: c[0]['seeders'], reverse=True)
		seen_hashes = set()
		for item, name, name_info in candidates[:self.MAX_TORRENTS]:
			try:
				tinfo = torrent_info(self._get(item['torrent'], binary=True))
				if not tinfo or tinfo['hash'] in seen_hashes: continue
				if is_archive_only(tinfo['files']): continue
				seen_hashes.add(tinfo['hash'])
				url = 'magnet:?xt=urn:btih:%s&dn=%s' % (tinfo['hash'], name)
				quality, info = source_utils.get_release_quality(name_info, url)
				dsize, isize = source_utils._size(item['size']) if item['size'] else (0, '')
				if not dsize and tinfo['size']:
					dsize = round(tinfo['size'] / 1073741824.0, 2); isize = '%.2f GB' % dsize
				if isize: info.insert(0, isize)
				sources.append({
					'source': 'torrent', 'language': 'en', 'direct': False, 'debridonly': True,
					'provider': 'yourbittorrent', 'hash': tinfo['hash'], 'url': url, 'name': name, 'name_info': name_info,
					'quality': quality, 'info': ' | '.join(info), 'size': dsize, 'seeders': item['seeders']
				})
			except Exception:
				source_utils.scraper_error('YOURBITTORRENT')
		return sources
