# -*- coding: utf-8 -*-
import json
import addonvar
from .utils import addDir

addon_icon = addonvar.addon_icon
addon_fanart = addonvar.addon_fanart
local_string = addonvar.local_string
buildfile = addonvar.buildfile
headers = addonvar.headers

def main_menu():
	addDir('Onze builds','',1,addon_icon,addon_fanart,local_string(30001),isFolder=True)
	addDir('Onderhoud','',5,addon_icon,addon_fanart,local_string(30002),isFolder=True)
	addDir('Frisse start','',4,addon_icon,addon_fanart,local_string(30003),isFolder=False)
	addDir('Mededelingen','',100,addon_icon,addon_fanart,'Bring up the notifications dialog',isFolder=False)
	addDir('Instellingen','',9,addon_icon,addon_fanart,local_string(30001),isFolder=False)

def build_menu():
    if buildfile.endswith('.xml'):
    	from .xml_parser import _xml
    	x = _xml(buildfile)
    	builds = json.loads(x.process_builds())['builds']
    elif buildfile.endswith('.json'):
    	from .json_parser import _json
    	j = _json(buildfile)
    	builds = json.loads(j.get_list())['builds']
    else:
    	addDir('URL ongeldig. Contact build bouwer.','','','','','',isFolder=False)
    	return
    for build in builds:
    	name = (build.get('name', 'Unknown'))
    	version = (build.get('version', '0'))
    	url = (build.get('url', ''))
    	icon = (build.get('icon', addon_icon))
    	fanart = (build.get('fanart', addon_fanart))
    	description = (build.get('description', 'Geen beschrijving beschikbaar.'))
    	if url.endswith('.xml') or url.endswith('.json'):
    		addDir(name,url,1,icon,fanart,description,name2=name,version=version,isFolder=True)
    	else:
    		addDir(name + ' Version ' + version,url,3,icon,fanart,description,name2=name,version=version,isFolder=False)

def submenu_maintenance():
	addDir('Packages map legen','',6,addon_icon,addon_fanart,local_string(30005),isFolder=False)
	addDir('Thumbnails map legen','',7,addon_icon,addon_fanart,local_string(30008),isFolder=False)
	addDir('Uitgereide instellingen','',8,addon_icon,addon_fanart,local_string(30009),isFolder=False)