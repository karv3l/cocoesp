# -*- coding: utf-8 -*-
"""
Puente: plugin://script.module.cocoscrapers/?action=... -> plugin://script.module.cocoesp/?action=...
"""
import sys
import xbmc

query = sys.argv[2] if len(sys.argv) > 2 else ''
query = query.replace('CocoScrapersSettings', 'cocoespSettings').replace('script.module.cocoscrapers', 'script.module.cocoesp')
xbmc.executebuiltin('RunPlugin(plugin://script.module.cocoesp/%s)' % query)
