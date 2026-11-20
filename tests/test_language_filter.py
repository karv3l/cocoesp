"""Pruebas del filtro de idioma (spec 001) sin Kodi ni red.

Extrae por AST de source_utils.py solo las constantes y las funciones puras necesarias,
así no se importa control.py (Kodi) ni se ejecuta ningún scraper.

Uso: .venv\\Scripts\\python -I tests\\test_language_filter.py
"""
import ast
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_UTILS = os.path.join(ROOT, 'src', 'script.module.cocoesp', 'lib', 'cocoesp', 'modules', 'source_utils.py')
FIXTURE = os.path.join(ROOT, 'tests', 'fixtures', 'torrentio_interstellar_es.json')
WANTED_FUNCS = {'remove_lang', 'is_spanish', 'has_spanish_flag', 'info_from_name'}


def load_subset():
    tree = ast.parse(open(SOURCE_UTILS, encoding='utf-8').read())
    nodes = [n for n in tree.body if
             (isinstance(n, ast.Assign) and all(isinstance(t, ast.Name) and t.id.isupper() for t in n.targets)) or
             (isinstance(n, ast.FunctionDef) and n.name in WANTED_FUNCS)]
    ns = {'re': re}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), 'source_utils_subset', 'exec'), ns)
    return ns


NS = load_subset()


def name_info(release, full_title=None):
    clean = re.sub(r'[^\x20-\x7e]', '', release).strip().replace(' ', '.')
    ni = NS['info_from_name'](clean, 'Interstellar', '2014')
    if full_title and NS['has_spanish_flag'](full_title): ni += NS['SPA_TAG']
    return ni


# (release, {modo: ¿se descarta?})  modo True = inglés con filtro de audio extranjero
CASES = [
    ('Interstellar.2014.1080p.BluRay.x264-SPARKS', {True: False, False: False, 'es': True, 'multi': False}),
    ('Interstellar.2014.1080p.SPANISH.BluRay', {True: True, False: False, 'es': False, 'multi': False}),
    ('Interstellar.2014.1080p.dual-lat.cinecalidad.mp4', {True: True, 'es': False, 'multi': False}),
    ('Interstellar.2014.FRENCH.1080p', {True: True, 'es': True, 'multi': False}),
    ('Interstellar.2014.1080p.VOSE', {'es': False}),
    ('Interstellar.2014.1080p.German.DUBBED', {True: True, False: True, 'es': True, 'multi': False}),
    ('Interstellar.2014.1080p.Español', {'es': False}),
    ('Interstellar.2014.1080p.Cast.AC3', {'es': False}),
    ('Interstellar.2014.Lastday.1080p', {'es': True}),  # 'lat' dentro de otra palabra no cuenta
]


def main():
    fails = 0
    for release, expected in CASES:
        ni = name_info(release)
        for mode, should_remove in expected.items():
            got = NS['remove_lang'](ni, mode)
            ok = got == should_remove
            fails += not ok
            print('%s %-50s modo=%-5s descarta=%s' % ('OK  ' if ok else 'FAIL', release, mode, got))

    streams = json.load(open(FIXTURE, encoding='utf-8'))['streams']
    kept = [s for s in streams if not NS['remove_lang'](name_info(s['title'].split('\n')[0], s['title']), 'es')]
    removed_pl = [s for s in streams if s not in kept]
    print('\nTorrentio (fixture, modo es): %d resultados, %d se mantienen, %d descartados' % (len(streams), len(kept), len(removed_pl)))
    # Todo lo que se mantiene debe llevar bandera española/mexicana; todo lo descartado, no
    for s in kept:
        if not NS['has_spanish_flag'](s['title']):
            fails += 1; print('FAIL se mantiene sin bandera ES/MX:', s['title'].split('\n')[0][:80])
    for s in removed_pl:
        if NS['has_spanish_flag'](s['title']):
            fails += 1; print('FAIL descartado con bandera ES/MX:', s['title'].split('\n')[0][:80])
    if (len(streams), len(kept)) != (20, 15):
        fails += 1; print('FAIL se esperaban 20 resultados y 15 mantenidos')

    print('\nFALLOS: %d' % fails)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
