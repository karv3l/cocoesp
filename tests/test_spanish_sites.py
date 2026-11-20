"""Pruebas de los proveedores de webs en castellano (spec 006) sin Kodi ni red.

- Carga modules/spanish_sites.py y los 4 proveedores por ruta (sin importar el paquete cocoesp).
- Sustituye la red (_request) por HTML y .torrent sintéticos y las utilidades de Kodi por dobles simples.
- El HTML es sintético: las webs están bloqueadas por DNS en la red de desarrollo, así que estas pruebas
  validan la lógica, no la maquetación real de cada web.

Uso: .venv\\Scripts\\python -I tests\\test_spanish_sites.py
"""
import hashlib
import importlib.util
import os
import re
import sys
import types

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.join(ROOT, 'src', 'script.module.cocoesp', 'lib', 'cocoesp')
PROVIDERS = ('dontorrent', 'elitetorrent', 'divxtotal', 'grantorrent')


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


for pkg in ('cocoesp', 'cocoesp.modules'):
    sys.modules.setdefault(pkg, types.ModuleType(pkg))
ss = load('cocoesp.modules.spanish_sites', os.path.join(LIB, 'modules', 'spanish_sites.py'))
providers = {p: load('prov_' + p, os.path.join(LIB, 'sources_cocoesp', 'torrents', p + '.py')).source for p in PROVIDERS}


# ------------------------------------------------------------------ dobles

def bencode(v):
    if isinstance(v, int): return b'i%de' % v
    if isinstance(v, str): v = v.encode()
    if isinstance(v, bytes): return b'%d:%s' % (len(v), v)
    if isinstance(v, list): return b'l' + b''.join(bencode(x) for x in v) + b'e'
    if isinstance(v, dict): return b'd' + b''.join(bencode(k) + bencode(v[k]) for k in sorted(v)) + b'e'
    raise TypeError(v)


def make_torrent(name, files):
    info = {'name': name, 'piece length': 262144, 'pieces': b'x' * 20}
    if len(files) == 1 and files[0][0] == name: info['length'] = files[0][1]
    else: info['files'] = [{'path': f.split('/'), 'length': n} for f, n in files]
    data = bencode({'announce': 'udp://tracker.example:80', 'info': info})
    return data, hashlib.sha1(bencode(info)).hexdigest()


class FakeUtils(object):
    errors = []
    @staticmethod
    def aliases_to_array(aliases, filter=None):
        countries = [filter] if isinstance(filter, str) else filter
        return [a if isinstance(a, str) else a.get('title', '') for a in aliases
                if isinstance(a, str) or not countries or a.get('country') in countries]
    get_undesirables = staticmethod(lambda: [])
    check_foreign_audio = staticmethod(lambda: 'es')
    clean_name = staticmethod(lambda n: n.replace(' ', '.'))
    info_from_name = staticmethod(lambda n, t, y, *a, **k: '.%s.' % re.sub(r'[^a-z0-9]+', '.', n.lower()).strip('.'))
    remove_lang = staticmethod(lambda ni, mode: not ni.endswith('spanish.'))
    remove_undesirables = staticmethod(lambda ni, u: False)
    get_release_quality = staticmethod(lambda ni, url: ('1080p' if '1080p' in ni else 'SD', []))
    @classmethod
    def scraper_error(cls, name): cls.errors.append(name)


def fake_provider(cls, pages):
    """Instancia del proveedor con red simulada: pages = {url o (url, post): str|bytes}."""
    class P(cls):
        requested = []
        def _custom_domain(self): return ''
        def _utils(self): return FakeUtils
        def _request(self, url, post=None, referer=None, binary=False):
            self.requested.append((url, post))
            return pages.get((url, post), pages.get(url))
    return P()


# ------------------------------------------------------------------ casos

fails = 0
def check(label, cond, extra=''):
    global fails
    fails += not cond
    print('%s %s%s' % ('OK  ' if cond else 'FAIL', label, ('  -> %s' % extra) if extra and not cond else ''))


DATA = {'title': 'The Godfather', 'year': '1972', 'imdb': 'tt0068646',
        'aliases': [{'title': 'El padrino', 'country': 'es'}, {'title': 'Il padrino', 'country': 'it'}]}

# bencode / torrent_info
t_single, h_single = make_torrent('El.Padrino.1972.1080p.BluRay.Castellano.mkv', [('El.Padrino.1972.1080p.BluRay.Castellano.mkv', 8 * 1073741824)])
info = ss.torrent_info(t_single)
check('torrent_info: hash = SHA-1 del dict info', info and info['hash'] == h_single)
check('torrent_info: nombre y tamaño', info and info['size'] == 8 * 1073741824 and info['name'].startswith('El.Padrino'))
t_rar, _ = make_torrent('El Padrino [Clave]', [('El Padrino [Clave]/pelicula.rar', 10 ** 9), ('El Padrino [Clave]/leeme.txt', 10)])
check('archivo solo .rar detectado', ss.is_archive_only(ss.torrent_info(t_rar)['files']))
check('HTML no es torrent', ss.torrent_info(b'<html>no</html>') is None)
check('torrent truncado no rompe', ss.torrent_info(t_single[:40]) is None)
check('magnet_info', ss.magnet_info('magnet:?xt=urn:btih:%s&dn=El+Padrino' % ('a' * 40))['name'] == 'El Padrino')

# títulos
names = {ss.norm_title(t) for t in ['The Godfather', 'El padrino', 'Il padrino']}
check('norm_title quita etiquetas y acentos', ss.norm_title('El Padrino (1972) [BluRay 1080p][Castellano]') == 'elpadrino')
check('title_matches acepta alias en español', ss.title_matches('El Padrino [4K UHDrip]', names, '1972'))
check('title_matches rechaza año lejano', not ss.title_matches('El Padrino (1990)', names, '1972'))
check('title_matches rechaza otro título', not ss.title_matches('El Padrino II', names, '1972'))
check('slug_text', ss.slug_text('https://x.com/pelicula/12345/el-padrino-1972/') == 'el padrino 1972')

# flujo completo por web
for prov, cls in providers.items():
    base = cls.default_domain.rstrip('/')
    detail = base + ('/pelicula/' if prov == 'dontorrent' else '/peliculas/') + '9876/el-padrino-1972/'
    other = base + ('/pelicula/' if prov == 'dontorrent' else '/peliculas/') + '5555/el-padrino-ii-1974/'
    tor_host = base.replace('https://', 'https://files.') if prov == 'grantorrent' else base
    search_html = ('<div><a href="%s">El Padrino (1972) [BluRay 1080p]</a><a href="%s">El Padrino II</a>'
                   '<a href="/contacto">Contacto</a><a href="https://otra-web.com/peliculas/el-padrino/">x</a></div>') % (detail, other)
    detail_html = ('<a class="btn" href="%s/torrents/el-padrino-1080p.torrent">Descargar</a>'
                   '<a href="%s/torrents/el-padrino-clave.torrent">Descargar RAR</a>') % (tor_host, tor_host)
    pages = {detail: detail_html,
             tor_host + '/torrents/el-padrino-1080p.torrent': t_single,
             tor_host + '/torrents/el-padrino-clave.torrent': t_rar}
    q = 'El+padrino'
    if cls.search_post is not None:
        pages[(base + cls.search_path, cls.search_post % 'The+Godfather')] = '<p>sin resultados</p>'
        pages[(base + cls.search_path, cls.search_post % q)] = search_html
    else:
        pages[base + cls.search_path % 'The+Godfather'] = '<p>sin resultados</p>'
        pages[base + cls.search_path % q] = search_html
    p = fake_provider(cls, pages)
    res = p.sources(dict(DATA), [])
    check('%-12s busca con título y alias es' % prov, [u for u, _ in p.requested][:2] == [base + (cls.search_path if cls.search_post else cls.search_path % s) for s in ('The+Godfather', q)],
          p.requested[:2])
    check('%-12s no abre la ficha de El Padrino II' % prov, all(other != u for u, _ in p.requested))
    check('%-12s 1 resultado (descarta el .rar)' % prov, len(res) == 1, res)
    if res:
        r = res[0]
        check('%-12s hash, magnet, tamaño y español' % prov, r['hash'] == h_single and r['url'].startswith('magnet:?xt=urn:btih:' + h_single)
              and r['size'] == 8.0 and r['name_info'].endswith('spanish.') and r['provider'] == prov and r['quality'] == '1080p', r)

# series y web caída
p = fake_provider(providers['elitetorrent'], {})
check('series: no busca', p.sources({'tvshowtitle': 'Los Serrano', 'title': 'x', 'year': '2003', 'aliases': []}, []) == [] and not p.requested)
check('web caída: lista vacía sin excepción', p.sources(dict(DATA), []) == [])
check('sin errores registrados', not FakeUtils.errors, FakeUtils.errors)

print('\nFALLOS: %d' % fails)
sys.exit(1 if fails else 0)
