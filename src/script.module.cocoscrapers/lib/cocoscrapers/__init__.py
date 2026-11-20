# -*- coding: utf-8 -*-
"""
Puente cocoscrapers -> cocoesp.

Las apps (Fen, Umbrella...) hacen "import cocoscrapers" / "from cocoscrapers.modules import ...".
Este paquete se sustituye a sí mismo por cocoesp en sys.modules y registra un buscador
que resuelve cualquier submódulo cocoscrapers.X como cocoesp.X (sources_cocoscrapers -> sources_cocoesp).
"""
import importlib
import importlib.abc
import importlib.util
import os
import sys

_TARGET = 'cocoesp'
_RENAMES = (('cocoscrapers.sources_cocoscrapers', 'cocoesp.sources_cocoesp'), ('cocoscrapers', 'cocoesp'))


def _target_name(name):
	for old, new in _RENAMES:
		if name == old or name.startswith(old + '.'):
			return new + name[len(old):]
	return None


class _AliasLoader(importlib.abc.Loader):
	def __init__(self, target):
		self.target = target

	def create_module(self, spec):
		return importlib.import_module(self.target)

	def exec_module(self, module):
		pass


class _AliasFinder(importlib.abc.MetaPathFinder):
	_cocoesp_alias = True

	def find_spec(self, name, path=None, target=None):
		if not name.startswith('cocoscrapers.'): return None
		target_name = _target_name(name)
		if not target_name: return None
		return importlib.util.spec_from_loader(name, _AliasLoader(target_name))


def _ensure_cocoesp_path():
	# Kodi añade al sys.path la carpeta lib de las dependencias; por si no lo hace con las transitivas
	if importlib.util.find_spec(_TARGET) is not None: return
	try:
		import xbmcaddon, xbmcvfs
		addon_path = xbmcvfs.translatePath(xbmcaddon.Addon('script.module.cocoesp').getAddonInfo('path'))
		sys.path.append(os.path.join(addon_path, 'lib'))
	except Exception:
		pass


_ensure_cocoesp_path()
if not any(getattr(f, '_cocoesp_alias', False) for f in sys.meta_path):
	sys.meta_path.insert(0, _AliasFinder())

sys.modules[__name__] = importlib.import_module(_TARGET)
