# -*- coding: utf-8 -*-
"""
	Fenomscrapers Module
"""

from cocoesp.modules.control import addonPath, addonVersion, joinPath
from cocoesp.windows.textviewer import TextViewerXML


def get(file):
	cocoesp_path = addonPath()
	cocoesp_version = addonVersion()
	helpFile = joinPath(cocoesp_path, 'lib', 'cocoesp', 'help', file + '.txt')
	r = open(helpFile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]cocoesp -  v%s - %s[/B]' % (cocoesp_version, file)
	windows = TextViewerXML('textviewer.xml', cocoesp_path, heading=heading, text=text)
	windows.run()
	del windows