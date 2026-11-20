"""Pruebas del alias de importación del add-on puente (spec 004) sin Kodi.

Crea un paquete «cocoesp» falso en un directorio temporal (no ejecuta los scrapers reales)
y comprueba que «cocoscrapers» y sus submódulos resuelven a los mismos objetos de cocoesp.
Cada comprobación se ejecuta en un intérprete nuevo para que sys.modules empiece limpio.

Uso: .venv\\Scripts\\python -I tests\\test_bridge_alias.py
"""
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRIDGE_LIB = os.path.join(ROOT, 'src', 'script.module.cocoscrapers', 'lib')

FAKE = {
    'cocoesp/__init__.py': "def sources(specified_folders=None, ret_all=False): return ['ok']\n",
    'cocoesp/modules/__init__.py': '',
    'cocoesp/modules/control.py': "def setting(x): return 'val-' + x\n",
    'cocoesp/sources_cocoesp/__init__.py': "all_providers = ['torrentio']\n",
    'cocoesp/sources_cocoesp/torrents/__init__.py': '',
    'cocoesp/sources_cocoesp/torrents/torrentio.py': "class source: name = 'torrentio'\n",
}

CHECKS = {
    'import cocoscrapers devuelve cocoesp':
        "import cocoscrapers, cocoesp; assert cocoscrapers is cocoesp",
    'from cocoscrapers import sources':
        "from cocoscrapers import sources; assert sources() == ['ok']",
    'submódulo cocoscrapers.modules.control':
        "from cocoscrapers.modules import control; import cocoesp.modules.control as r; assert control is r and control.setting('x') == 'val-x'",
    'from cocoscrapers.modules.control import setting':
        "from cocoscrapers.modules.control import setting; assert setting('y') == 'val-y'",
    'sources_cocoscrapers -> sources_cocoesp':
        "from cocoscrapers import sources_cocoscrapers as s; assert s.all_providers == ['torrentio']",
    'proveedor por ruta completa':
        "import cocoscrapers.sources_cocoscrapers.torrents.torrentio as t, cocoesp.sources_cocoesp.torrents.torrentio as t2; assert t is t2",
    'módulo inexistente da ModuleNotFoundError':
        "import cocoscrapers\ntry:\n    import cocoscrapers.noexiste\n    raise SystemExit(1)\nexcept ModuleNotFoundError:\n    pass",
    'importar dos veces no duplica el buscador':
        "import sys, importlib, cocoscrapers; sys.modules.pop('cocoscrapers'); import cocoscrapers; "
        "assert sum(getattr(f, '_cocoesp_alias', False) for f in sys.meta_path) == 1",
}


def main():
    fails = 0
    with tempfile.TemporaryDirectory() as fake_dir:
        for rel, content in FAKE.items():
            path = os.path.join(fake_dir, *rel.split('/'))
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f: f.write(content)
        for label, code in CHECKS.items():
            prog = 'import sys; sys.path[:0] = [%r, %r]\n%s' % (BRIDGE_LIB, fake_dir, code)
            r = subprocess.run([sys.executable, '-I', '-B', '-c', prog], capture_output=True, text=True)
            ok = r.returncode == 0
            fails += not ok
            print('%s %s%s' % ('OK  ' if ok else 'FAIL', label, '' if ok else '\n' + r.stderr.strip()[-400:]))
    print('\nFALLOS: %d' % fails)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
