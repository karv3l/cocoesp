# -*- coding: utf-8 -*-
"""
	Fenomscrapers Module
"""

from cocoesp.modules.control import addonPath, addonVersion, joinPath
from cocoesp.windows.textviewer import TextViewerXML


def get():
	cocoesp_path = addonPath()
	cocoesp_version = addonVersion()
	changelogfile = joinPath(cocoesp_path, 'changelog.txt')
	r = open(changelogfile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]cocoesp -  v%s - ChangeLog[/B]' % cocoesp_version
	windows = TextViewerXML('textviewer.xml', cocoesp_path, heading=heading, text=text)
	windows.run()
	del windows