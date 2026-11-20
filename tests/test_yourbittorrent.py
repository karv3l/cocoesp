"""Pruebas del proveedor YourBittorrent (spec 007) sin Kodi ni red.

Carga el source_utils REAL de cocoesp (check_title, info_from_name, remove_lang...) con dobles
mínimos de Kodi, y sirve como red los RSS reales capturados en tests/fixtures/yourbittorrent/.
Los .torrent son sintéticos (uno por id de enclosure).

Uso: .venv\\Scripts\\python -I tests\\test_yourbittorrent.py
"""
import hashlib
import importlib.util
import os
import re
import sys
import types
from urllib.parse import quote_plus

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.join(ROOT, 'src', 'script.module.cocoesp', 'lib', 'cocoesp')
FIX = os.path.join(ROOT, 'tests', 'fixtures', 'yourbittorrent')
SETTINGS = {'filter.language': '1', 'filter.undesirables': 'false', 'filter.foreign.single.audio': 'true'}
NETWORK = {}
ERRORS = []


def stub(name, **attrs):
	m = types.ModuleType(name); m.__dict__.update(attrs); sys.modules[name] = m
	parent, _, child = name.rpartition('.')
	if parent: setattr(sys.modules[parent], child, m)
	return m


def load(name, path):
	spec = importlib.util.spec_from_file_location(name, path)
	m = importlib.util.module_from_spec(spec); sys.modules[name] = m
	parent, _, child = name.rpartition('.')
	if parent in sys.modules: setattr(sys.modules[parent], child, m)
	spec.loader.exec_module(m)
	return m


# ---- dobles de Kodi y red
stub('cocoesp'); stub('cocoesp.modules')
stub('cocoesp.modules.control', homeWindow=types.SimpleNamespace(getProperty=lambda k: ''),
	 setting=lambda k, d=None: SETTINGS.get(k, ''), setSetting=lambda k, v: None)
stub('cocoesp.modules.undesirables', Undesirables=type('Undesirables', (), {'get_enabled': lambda self: []}))
stub('cocoesp.modules.log_utils', log=lambda *a, **k: ERRORS.append(a), error=lambda *a, **k: ERRORS.append(a), LOGERROR=4)


class Resp(object):
	def __init__(self, body):
		self.status_code = 200 if body is not None else 404
		self.content = body if isinstance(body, bytes) else (body or '').encode('utf-8')
		self.text = body if isinstance(body, str) else ''


def bencode(v):
	if isinstance(v, int): return b'i%de' % v
	if isinstance(v, str): v = v.encode()
	if isinstance(v, bytes): return b'%d:%s' % (len(v), v)
	if isinstance(v, list): return b'l' + b''.join(bencode(x) for x in v) + b'e'
	return b'd' + b''.join(bencode(k) + bencode(v[k]) for k in sorted(v)) + b'e'


def fake_request(method, url, headers=None, timeout=None, **kw):
	NETWORK.setdefault('log', []).append(url)
	m = re.match(r'https://yt\.t0r\.store/down/(\d+)\.torrent', url)
	if m:
		info = {'name': 'movie%s.mkv' % m.group(1), 'length': 2 * 1073741824, 'piece length': 262144, 'pieces': b'x' * 20}
		return Resp(bencode({'info': info}))
	return Resp(NETWORK.get(url))


stub('cocoesp.modules.coco_client', randomagent=lambda: 'test-agent',
	 session=types.SimpleNamespace(request=fake_request))
load('cocoesp.modules.cleantitle', os.path.join(LIB, 'modules', 'cleantitle.py'))
su = load('cocoesp.modules.source_utils', os.path.join(LIB, 'modules', 'source_utils.py'))
load('cocoesp.modules.coco_compat', os.path.join(LIB, 'modules', 'coco_compat.py'))
load('cocoesp.modules.spanish_sites', os.path.join(LIB, 'modules', 'spanish_sites.py'))
ybt = load('prov_yourbittorrent', os.path.join(LIB, 'sources_cocoesp', 'torrents', 'yourbittorrent.py'))


def rss(fname): return open(os.path.join(FIX, fname), encoding='utf-8').read()
def q(text): return 'https://yourbittorrent.com/rss.xml?q=' + quote_plus(text)


fails = 0
def check(label, cond, extra=''):
	global fails
	fails += not cond
	print('%s %s%s' % ('OK  ' if cond else 'FAIL', label, ('  -> %s' % (extra,)) if extra and not cond else ''))


# ---- parse_rss con RSS real
items = ybt.parse_rss(rss('interstellar_2014.xml'))
check('parse_rss: 30 items con torrent, semillas y tamaño', len(items) == 30 and all(i['torrent'].endswith('.torrent') for i in items)
	  and any(i['seeders'] > 0 for i in items) and items[0]['size'].endswith('GB'), items[:1])

GODFATHER = {'title': 'The Godfather', 'year': '1972', 'imdb': 'tt0068646',
			 'aliases': [{'title': 'El padrino', 'country': 'es'}, {'title': 'Il padrino', 'country': 'it'}]}
NETWORK.update({q('The Godfather 1972'): rss('the_godfather_1972.xml'), q('The Godfather spa'): rss('the_godfather_spa.xml')})

# ---- modo Solo español: El Padrino (descartes)
SETTINGS['filter.language'] = '1'; NETWORK['log'] = []
res = ybt.source().sources(dict(GODFATHER), [])
searched = [u for u in NETWORK['log'] if 'rss.xml' in u]
check('es: consultas título+año, «spa» y alias es', searched == [q('The Godfather 1972'), q('The Godfather spa'), q('El padrino 1972')], searched)
check('es: descarta Dual.PTBR (portugués) y «The Godfather I/II/III»', res == [], [r['name'] for r in res])

# ---- modo Solo español: Interstellar (positivo)
INTERSTELLAR = {'title': 'Interstellar', 'year': '2014', 'imdb': 'tt0816692', 'aliases': []}
NETWORK.update({q('Interstellar 2014'): rss('interstellar_2014.xml'), q('Interstellar spa'): rss('interstellar_spa.xml')})
NETWORK['log'] = []
res = ybt.source().sources(dict(INTERSTELLAR), [])
names = [r['name'] for r in res]
check('es: encuentra el remux multi-idioma con Spa', any('Spa' in n and 'Remux' in n for n in names), names)
check('es: todos con marca de español', all(su.is_spanish(r['name_info']) for r in res), names)
check('es: hash calculado del .torrent y magnet', res and all(len(r['hash']) == 40 and r['url'].startswith('magnet:?xt=urn:btih:' + r['hash']) for r in res))
check('es: máximo 10 torrents descargados', sum('t0r.store' in u for u in NETWORK['log']) <= 10)

# ---- modo Inglés: sin «spa» y sin descartar por no ser español
SETTINGS['filter.language'] = '0'; NETWORK['log'] = []
res_en = ybt.source().sources(dict(GODFATHER), [])
searched = [u for u in NETWORK['log'] if 'rss.xml' in u]
check('en: una sola consulta título+año', searched == [q('The Godfather 1972')], searched)
check('en: devuelve resultados', len(res_en) > 0)

# ---- caídas
NETWORK.clear(); SETTINGS['filter.language'] = '1'
check('RSS caído: lista vacía', ybt.source().sources(dict(GODFATHER), []) == [])
check('sin errores registrados', not ERRORS, ERRORS[:2])

print('\nFALLOS: %d' % fails)
sys.exit(1 if fails else 0)
