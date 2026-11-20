# -*- coding: utf-8 -*-
"""
Base común para proveedores de webs de torrents en castellano (spec 006).

Flujo: búsqueda en la web -> fichas de película -> enlaces .torrent/magnet -> infohash.
La configuración de cada web (dominio, búsqueda, rutas) se basa en los canales de
Alfa (https://github.com/alfa-addon/addon, GPL-3.0). No resuelve captchas ni pruebas antibot.

No importa nada de Kodi a nivel de módulo: así se puede probar fuera de Kodi.
"""
import hashlib
import re
import unicodedata
from urllib.parse import quote_plus, unquote, urljoin, urlparse

MAX_PAGES = 5
MAX_TORRENTS = 10
ARCHIVE_EXT = ('.rar', '.zip', '.7z', '.r00', '.001')
VIDEO_EXT = ('.mkv', '.mp4', '.avi', '.m2ts', '.ts', '.iso', '.wmv', '.mov', '.mpg', '.mpeg', '.vob', '.m4v', '.divx')

_TAG_WORDS = re.compile(
	r'\b(?:4k|uhd|hdr10?|3d|imax|full ?bluray|bluray|blu ray|bdrip|bdremux|remux|microhd|hdrip|dvdrip|dvdscr|'
	r'web ?dl|webrip|web|hdtv|2160p|1080p|720p|480p|x264|x265|hevc|castellano|espanol|spanish|latino|dual|'
	r'subtitulado|subs|vose|vos|completa|extendida|version extendida|ac3|dts|5 1)\b')
_LINK_RE = re.compile(r'<a\s[^>]*?href\s*=\s*["\']([^"\']+)["\'][^>]*>(.*?)</a\s*>', re.I | re.S)
_TITLE_ATTR_RE = re.compile(r'title\s*=\s*["\']([^"\']+)["\']', re.I)
_YEAR_RE = re.compile(r'\b(19\d{2}|20\d{2})\b')


# --------------------------------------------------------------------------- bencode / torrent

class BencodeError(ValueError):
	pass


def bdecode(data):
	"""Decodifica bencode. Devuelve (valor, (inicio, fin)) donde la tupla es el tramo
	en bytes del diccionario 'info' de primer nivel (o None)."""
	info_span = []

	def dec(i, depth):
		c = data[i:i + 1]
		if c == b'i':
			end = data.index(b'e', i)
			return int(data[i + 1:end]), end + 1
		if c == b'l':
			i += 1; out = []
			while data[i:i + 1] != b'e':
				if i >= len(data): raise BencodeError('lista sin cerrar')
				v, i = dec(i, depth + 1); out.append(v)
			return out, i + 1
		if c == b'd':
			i += 1; out = {}
			while data[i:i + 1] != b'e':
				if i >= len(data): raise BencodeError('diccionario sin cerrar')
				k, i = dec(i, depth + 1)
				start = i
				v, i = dec(i, depth + 1)
				if depth == 0 and k == b'info' and not info_span: info_span.append((start, i))
				out[k] = v
			return out, i + 1
		if c.isdigit():
			colon = data.index(b':', i)
			n = int(data[i:colon]); start = colon + 1
			if start + n > len(data): raise BencodeError('cadena truncada')
			return data[start:start + n], start + n
		raise BencodeError('byte inesperado en %d' % i)

	value, _ = dec(0, 0)
	return value, (info_span[0] if info_span else None)


def _txt(b):
	if isinstance(b, bytes): return b.decode('utf-8', 'replace')
	return str(b)


def torrent_info(data):
	"""{'hash','name','size','files'} de un .torrent en bytes, o None si no es un torrent válido."""
	try:
		if not data or data[:1] != b'd': return None
		meta, span = bdecode(data)
		info = meta.get(b'info')
		if not isinstance(info, dict) or not span: return None
		name = _txt(info.get(b'name.utf-8') or info.get(b'name') or b'')
		if b'files' in info:
			files = [('/'.join(_txt(p) for p in (f.get(b'path.utf-8') or f.get(b'path') or [])), int(f.get(b'length', 0)))
					 for f in info[b'files']]
		else:
			files = [(name, int(info.get(b'length', 0)))]
		return {'hash': hashlib.sha1(data[span[0]:span[1]]).hexdigest(), 'name': name,
				'size': sum(size for _, size in files), 'files': files}
	except Exception:
		return None


def is_archive_only(files):
	"""True si no hay ningún vídeo y sí algún comprimido (suele ir con contraseña)."""
	names = [f[0].lower() for f in files]
	return not any(n.endswith(VIDEO_EXT) for n in names) and any(n.endswith(ARCHIVE_EXT) for n in names)


def magnet_info(link):
	h = re.search(r'btih:([a-fA-F0-9]{40}|[A-Za-z2-7]{32})', link)
	if not h: return None
	dn = re.search(r'[?&]dn=([^&]+)', link)
	return {'hash': h.group(1).lower(), 'name': unquote(dn.group(1)).replace('+', ' ') if dn else '', 'size': 0, 'files': []}


# --------------------------------------------------------------------------- títulos y enlaces

def strip_accents(text):
	text = unicodedata.normalize('NFKD', text or '')
	return ''.join(c for c in text if not unicodedata.combining(c))


def norm_title(text):
	"""Título comparable: sin acentos, etiquetas entre corchetes/paréntesis, años ni palabras de calidad/idioma."""
	if not text: return ''
	text = strip_accents(text).lower().replace('&amp;', '&')
	text = re.sub(r'\[.*?\]|\(.*?\)|\{.*?\}', ' ', text)
	text = _YEAR_RE.sub(' ', text)
	text = re.sub(r'[^a-z0-9]+', ' ', text)
	text = _TAG_WORDS.sub(' ', text)
	return re.sub(r'[^a-z0-9]+', '', text)


def extract_year(text):
	m = _YEAR_RE.search(text or '')
	return int(m.group(1)) if m else None


def slug_text(url):
	"""Texto legible del último segmento de una URL ('12345-interstellar-2014' -> 'interstellar 2014')."""
	seg = [s for s in urlparse(url).path.split('/') if s]
	if not seg: return ''
	tokens = [t for t in unquote(seg[-1]).replace('.html', '').split('-') if t and not (t.isdigit() and len(t) != 4)]
	return ' '.join(tokens)


def title_matches(text, names, year):
	if norm_title(text) not in names: return False
	found = extract_year(text)
	try:
		if found and year and abs(found - int(year)) > 1: return False
	except ValueError:
		pass
	return True


def _strip_tags(html):
	return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', html or '')).strip()


def find_links(html, base, path_re):
	"""[(url_absoluta, texto)] de los enlaces del mismo dominio cuyo path casa con path_re."""
	if not html: return []
	host = urlparse(base).netloc.lower().replace('www.', '')
	out, seen = [], set()
	for m in _LINK_RE.finditer(html):
		href = m.group(1).strip()
		if href.startswith(('#', 'javascript:', 'magnet:')): continue
		url = urljoin(base + '/', href)
		p = urlparse(url)
		if host and host not in p.netloc.lower(): continue
		if not re.search(path_re, p.path, re.I): continue
		if url in seen: continue
		seen.add(url)
		attr = _TITLE_ATTR_RE.search(m.group(0))
		text = _strip_tags(m.group(2)) or (attr.group(1) if attr else '')
		out.append((url, text))
	return out


def find_torrent_links(html, page_url, torrent_re=r'\.torrent(?:$|[?#])'):
	"""Enlaces magnet y .torrent de una ficha, en orden de aparición y sin duplicados."""
	if not html: return []
	out = []
	for m in re.finditer(r'(?:href|data-href|data-url)\s*=\s*["\']([^"\']+)["\']', html, re.I):
		href = m.group(1).strip().replace('&amp;', '&')
		if href.startswith('magnet:'): link = href
		else:
			link = urljoin(page_url, href)
			if not re.search(torrent_re, urlparse(link).path + ('?' + urlparse(link).query if urlparse(link).query else ''), re.I): continue
		if link not in out: out.append(link)
	return out


# --------------------------------------------------------------------------- proveedor base

class SpanishTorrentSite(object):
	"""Subclase por web: define site_name, url_setting, default_domain, search_path,
	search_post (None = GET), movie_link_re y, si hace falta, torrent_link_re."""
	timeout = 10
	priority = 2
	pack_capable = False
	hasMovies = True
	hasEpisodes = False
	site_name = ''
	url_setting = ''
	default_domain = ''
	search_path = '/?s=%s'
	search_post = None
	movie_link_re = r'/peliculas?/[^/?#]+'
	torrent_link_re = r'\.torrent(?:$|[?#])'

	def __init__(self):
		self.language = ['en', 'es']
		self.base_link = self._domain()

	# -- dependencias de Kodi (aisladas para poder sustituirlas en pruebas)
	def _custom_domain(self):
		try:
			from cocoesp.modules.control import setting
			return (setting(self.url_setting) or '').strip()
		except Exception:
			return ''

	def _utils(self):
		from cocoesp.modules import coco_compat
		return coco_compat

	def _request(self, url, post=None, referer=None, binary=False):
		from cocoesp.modules import coco_client as client
		headers = {'User-Agent': client.randomagent(), 'Referer': referer or self.base_link + '/'}
		if post is not None:
			headers['Content-Type'] = 'application/x-www-form-urlencoded'
			r = client.session.request('post', url, data=post, headers=headers, timeout=self.timeout)
		else:
			r = client.session.request('get', url, headers=headers, timeout=self.timeout)
		if r.status_code != 200: return None
		return r.content if binary else r.text

	# -- lógica
	def _domain(self):
		d = self._custom_domain() or self.default_domain
		if d and not d.startswith('http'): d = 'https://' + d
		return d.rstrip('/')

	def _get(self, url, post=None, referer=None, binary=False):
		try:
			return self._request(url, post=post, referer=referer, binary=binary)
		except Exception:
			return None

	def _search(self, term):
		q = quote_plus(term)
		if self.search_post is not None:
			return self._get(self.base_link + self.search_path, post=self.search_post % q)
		return self._get(self.base_link + self.search_path % q)

	def _search_terms(self, su, data):
		title = data['title']
		es_aliases = su.aliases_to_array(data.get('aliases') or [], ['es'])
		terms, seen = [], set()
		for t in [title] + list(es_aliases):
			n = norm_title(t)
			if t and n and n not in seen:
				seen.add(n); terms.append(t)
		return terms[:2]

	def sources(self, data, hostDict):
		sources = []
		if not data or 'tvshowtitle' in data or not self.base_link: return sources
		su = self._utils()
		try:
			if 'timeout' in data: self.timeout = int(data['timeout'])
			title, year = data['title'], str(data.get('year') or '')
			names = {norm_title(t) for t in [title] + list(su.aliases_to_array(data.get('aliases') or [])) if norm_title(t)}
			terms = self._search_terms(su, data)
			undesirables = su.get_undesirables()
			check_foreign_audio = su.check_foreign_audio()
		except Exception:
			su.scraper_error(self.site_name.upper())
			return sources

		pages = []
		for term in terms:
			for url, text in find_links(self._search(term), self.base_link, self.movie_link_re):
				if url in pages: continue
				if not (title_matches(text, names, year) or title_matches(slug_text(url), names, year)): continue
				pages.append(url)
				if len(pages) >= MAX_PAGES: break
			if len(pages) >= MAX_PAGES: break

		links = []
		for page in pages:
			for link in find_torrent_links(self._get(page), page, self.torrent_link_re):
				if all(link != l for l, _ in links): links.append((link, page))
		seen_hashes = set()
		for link, page in links[:MAX_TORRENTS]:
			try:
				if link.startswith('magnet:'): tinfo = magnet_info(link)
				else: tinfo = torrent_info(self._get(link, referer=page, binary=True))
				if not tinfo or tinfo['hash'] in seen_hashes: continue
				if tinfo['files'] and is_archive_only(tinfo['files']): continue
				seen_hashes.add(tinfo['hash'])
				name = su.clean_name(tinfo['name'] or slug_text(page)) or slug_text(page)
				name_info = su.info_from_name(name, title, year) + 'spanish.'
				if su.remove_lang(name_info, check_foreign_audio): continue
				if undesirables and su.remove_undesirables(name_info, undesirables): continue
				url = 'magnet:?xt=urn:btih:%s&dn=%s' % (tinfo['hash'], quote_plus(name))
				quality, info = su.get_release_quality(name_info, url)
				dsize = round(tinfo['size'] / 1073741824.0, 2) if tinfo['size'] else 0
				if dsize: info.insert(0, '%.2f GB' % dsize)
				sources.append({
					'source': 'torrent', 'language': 'en', 'direct': False, 'debridonly': True,
					'provider': self.site_name, 'hash': tinfo['hash'], 'url': url, 'name': name, 'name_info': name_info,
					'quality': quality, 'info': ' | '.join(info), 'size': dsize, 'seeders': 0
				})
			except Exception:
				su.scraper_error(self.site_name.upper())
		return sources
