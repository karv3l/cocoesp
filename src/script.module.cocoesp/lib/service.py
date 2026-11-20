# -*- coding: utf-8 -*-
"""
	Fenomscrapers Module
"""

import xbmc
from cocoesp.modules import control
from cocoesp.modules.Thread_pool import shutdown_executor
window = control.homeWindow
LOGINFO = 1 # (LOGNOTICE(2) deprecated in 19, use LOGINFO(1))

class CheckSettingsFile:
	def run(self):
		try:
			xbmc.log('[ script.module.cocoesp ]  CheckSettingsFile Service Starting...', LOGINFO)
			window.clearProperty('cocoesp')
			profile_dir = control.dataPath
			if not control.existsPath(profile_dir):
				success = control.makeDirs(profile_dir)
				if success: xbmc.log('%s : created successfully' % profile_dir, LOGINFO)
			else: xbmc.log('%s : already exists' % profile_dir, LOGINFO)
			settings_xml = control.joinPath(profile_dir, 'settings.xml')
			if not control.existsPath(settings_xml):
				control.setSetting('module.provider', 'cocoesp')
				xbmc.log('%s : created successfully' % settings_xml, LOGINFO)
			else: xbmc.log('%s : already exists' % settings_xml, LOGINFO)
			return xbmc.log('[ script.module.cocoesp ]  Finished CheckSettingsFile Service', LOGINFO)
		except:
			import traceback
			traceback.print_exc()

class SettingsMonitor(control.monitor_class):
	def __init__ (self):
		control.monitor_class.__init__(self)
		window.setProperty('cocoesp.debug.reversed', control.setting('debug.reversed'))
		xbmc.log('[ script.module.cocoesp ]  Settings Monitor Service Starting...', LOGINFO)

	def onSettingsChanged(self): # Kodi callback when the addon settings are changed
		window.clearProperty('cocoesp')
		control.sleep(50)
		refreshed = control.make_settings_dict()
		control.refresh_debugReversed()

class CheckUndesirablesDatabase:
	def run(self):
		xbmc.log('[ script.module.cocoesp ]  "CheckUndesirablesDatabase" Service Starting...', LOGINFO)
		from cocoesp.modules import undesirables
		try:
			old_database = undesirables.Undesirables().check_database()
			if old_database: undesirables.add_new_default_keywords()
		except:
			import traceback
			traceback.print_exc()
		return xbmc.log('[ script.module.cocoesp ]  Finished "CheckUndesirablesDatabase" Service', LOGINFO)

def main():
	while not control.monitor.abortRequested():
		xbmc.log('[ script.module.cocoesp ]  Service Started', LOGINFO)
		CheckSettingsFile().run()
		CheckUndesirablesDatabase().run()
		if control.isVersionUpdate():
			control.clean_settings()
			xbmc.log('[ script.module.cocoesp ]  Settings file cleaned complete', LOGINFO)
		break
	SettingsMonitor().waitForAbort()
	shutdown_executor()
	xbmc.log('[ script.module.cocoesp ]  Service Stopped', LOGINFO)

main()