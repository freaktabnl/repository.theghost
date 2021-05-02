import os
import addonvar
import xbmcgui
from .downloader import Downloader
from zipfile import ZipFile
from .save_data import save_check, save_backup,save_restore
from .maintenance import fresh_start

dp = addonvar.dp
dialog = addonvar.dialog
zippath = addonvar.zippath
addon_name = addonvar.addon_name
home = addonvar.home
setting_set = addonvar.setting_set
sleep = addonvar.sleep
headers = addonvar.headers

def main(NAME, NAME2, VERSION, URL, ICON, FANART, DESCRIPTION):
	
	yesInstall = dialog.yesno(NAME, 'Onze wizard is klaar om uw build te installeren.', nolabel='Annuleer', yeslabel='Ga door')
	if yesInstall:
	    save_check()
	    save_backup()
	    yesFresh = dialog.yesno('Frisse start', 'All data wordt nu eerst verwijderd', nolabel='Stop', yeslabel='Ga door')
	    if yesFresh:
	    	fresh_start()
	    	
	    build_install(NAME, NAME2, VERSION, URL)
	else:
		return

def build_install(name, name2, version, url):
	if os.path.exists(zippath):
		os.unlink(zippath)
	d = Downloader(url)
	if 'dropbox' in url:
		import xbmc
		if not xbmc.getCondVisibility('System.HasAddon(script.module.requests)'):
			xbmc.executebuiltin('InstallAddon(script.module.requests)')
			dialog.ok(name, 'Requests is being installed.\n Try again when Requests is finished installing.')
			return
		d.download_build(name,zippath,meth='requests')
	else:
		d.download_build(name, zippath, meth='urllib')
	if os.path.exists(zippath):
		dp.create(addon_name, 'Bestanden uitpakken...')
		dp.update(66, 'Bestanden uitpakken...')
		zf = ZipFile(zippath)
		zf.extractall(path = home)
		dp.update(100, 'Uitpakken bestanden...Gereed!')
		zf.close()
		os.unlink(zippath)
		save_restore()
		setting_set('buildname', name2)
		setting_set('buildversion', version)
		setting_set('firstrun', 'true')
		dialog.ok(addon_name, 'Installatie compleet. Klik nu op OK om Kodi af tes sluiten.')
		os._exit(1)
	else:
		return