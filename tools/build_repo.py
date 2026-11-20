"""Genera el repositorio de Kodi de karv3l a partir de los add-ons en src/.

Uso (desde C:\\Proyectos\\cocoesp):
    .venv\\Scripts\\python tools\\build_repo.py

Por cada carpeta de src/ con addon.xml crea zips/<id>/<id>-<version>.zip y copia
addon.xml, icon.png, fanart.png y changelog.txt al lado (Kodi los usa en la ficha del add-on).
Después regenera zips/addons.xml + addons.xml.md5, y en la raíz deja el zip del
add-on repositorio y un index.html para instalarlo desde el gestor de archivos de Kodi.
Los zips de versiones anteriores se conservan.
"""
import hashlib
import os
import re
import shutil
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'src')
OUT = ROOT  # la raíz del repo de GitHub karv3l/cocoesp es también el repositorio de Kodi
ZIPS = os.path.join(OUT, 'zips')
REPO_ADDON_ID = 'repository.karv3l'

EXCLUDE_DIRS = {'__pycache__', '.git', '__MACOSX', '.idea', '.vscode'}
EXCLUDE_FILES = {'.DS_Store', 'Thumbs.db', '.gitignore'}
EXCLUDE_EXT = ('.pyc', '.pyo')
SIDE_FILES = ('addon.xml', 'icon.png', 'fanart.png', 'changelog.txt')


def read_addon(addon_dir):
    root = ET.parse(os.path.join(addon_dir, 'addon.xml')).getroot()
    return root.get('id'), root.get('version')


def make_zip(addon_dir, addon_id, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for base, dirs, files in os.walk(addon_dir):
            dirs[:] = sorted(d for d in dirs if d not in EXCLUDE_DIRS)
            for name in sorted(files):
                if name in EXCLUDE_FILES or name.endswith(EXCLUDE_EXT):
                    continue
                full = os.path.join(base, name)
                rel = os.path.relpath(full, addon_dir).replace(os.sep, '/')
                zf.write(full, '%s/%s' % (addon_id, rel))


def addon_xml_body(addon_dir):
    with open(os.path.join(addon_dir, 'addon.xml'), encoding='utf-8') as f:
        text = f.read()
    text = re.sub(r'^\s*<\?xml[^>]*\?>\s*', '', text)
    return text.strip()


def main():
    addons = []
    for name in sorted(os.listdir(SRC)):
        addon_dir = os.path.join(SRC, name)
        if not os.path.isfile(os.path.join(addon_dir, 'addon.xml')):
            continue
        addon_id, version = read_addon(addon_dir)
        if addon_id != name:
            sys.exit('La carpeta %s no coincide con el id %s' % (name, addon_id))
        dest = os.path.join(ZIPS, addon_id)
        os.makedirs(dest, exist_ok=True)
        zip_path = os.path.join(dest, '%s-%s.zip' % (addon_id, version))
        make_zip(addon_dir, addon_id, zip_path)
        for side in SIDE_FILES:
            if os.path.isfile(os.path.join(addon_dir, side)):
                shutil.copy2(os.path.join(addon_dir, side), dest)
        addons.append((addon_id, version, addon_dir, zip_path))
        print('zip  %s' % os.path.relpath(zip_path, ROOT))

    xml = "<?xml version='1.0' encoding='utf-8'?>\n<addons>\n%s\n</addons>\n" % '\n'.join(
        addon_xml_body(d) for _, _, d, _ in addons)
    with open(os.path.join(ZIPS, 'addons.xml'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(xml)
    ET.parse(os.path.join(ZIPS, 'addons.xml'))  # falla si el XML combinado no es válido
    md5 = hashlib.md5(xml.encode('utf-8')).hexdigest()
    with open(os.path.join(ZIPS, 'addons.xml.md5'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(md5)
    print('addons.xml (%d add-ons), md5 %s' % (len(addons), md5))

    repo = [a for a in addons if a[0] == REPO_ADDON_ID]
    if repo:
        _, version, _, zip_path = repo[0]
        root_zip = os.path.basename(zip_path)
        for old in os.listdir(OUT):
            if old.startswith(REPO_ADDON_ID + '-') and old.endswith('.zip') and old != root_zip:
                os.remove(os.path.join(OUT, old))
        shutil.copy2(zip_path, os.path.join(OUT, root_zip))
        with open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8', newline='\n') as f:
            f.write('<!DOCTYPE html>\n<a href="%s">%s</a>\n' % (root_zip, root_zip))
        print('raiz %s + index.html' % root_zip)


if __name__ == '__main__':
    main()
