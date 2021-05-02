import os, shutil
import addonvar

EXCLUDES = addonvar.EXCLUDES
user_path = addonvar.user_path
data_path = addonvar.data_path
setting = addonvar.setting
addon_id = addonvar.addon_id
packages = addonvar.packages

def backup(path, file):
	if os.path.exists(os.path.join(path, file)):
		shutil.move(os.path.join(path, file), os.path.join(packages, file))

def restore(path, file):
	if os.path.exists(os.path.join(packages, file)):
		if os.path.exists(os.path.join(path, file)):
			os.remove(os.path.join(path, file))
		shutil.move(os.path.join(packages, file), os.path.join(path, file))

def save_check():
	if setting('savefavs')=='true':
		EXCLUDES.append('favourites.xml')
	if setting('savesources')=='true':
		EXCLUDES.append('sources.xml')
	if setting('savedebrid')=='true':
		EXCLUDES.append('script.module.resolveurl')
	if setting('saveadvanced')=='true':
		EXCLUDES.append('advancedsettings.xml')
	return EXCLUDES

def save_backup():
	backup(user_path, addon_id)
	if setting('savefavs')=='true':
		backup(user_path, 'favourites.xml')
	if setting('savesources')=='true':
		backup(user_path, 'sources.xml')
	if setting('savedebrid')=='true':
		backup(data_path, 'script.module.resolveurl')
	if setting('saveadvanced')=='true':
		backup(user_path, 'advancedsettings.xml')

def save_restore():
	restore(user_path, addon_id)
	if setting('savefavs')=='true':
		restore(user_path, 'favourites.xml')
	if setting('savesources')=='true':
		restore(user_path, 'sources.xml')
	if setting('savedebrid')=='true':
		restore(data_path, 'script.module.resolveurl')
	if setting('saveadvanced')=='true':
		restore(user_path, 'advancedsettings.xml')
	shutil.rmtree(packages)