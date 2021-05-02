# -*- coding: utf-8 -*-
'''#####-----XBMC Library Modules-----#####'''
import xbmc
import xbmcgui
import xbmcplugin

'''######------External Modules-----#####'''
from inspect import getframeinfo, stack
import sys
from urllib.parse import quote_plus

'''#####-----Internal Modules-----#####'''
from addonvar import setting_true,addon_name,addon_version

def addDir(name,url,mode,iconimage,fanart,description, name2='', version='', addcontext=False,isFolder=True):
	u=sys.argv[0]+"?url="+quote_plus(url)+"&mode="+str(mode)+"&name="+quote_plus(name)+"&icon="+quote_plus(iconimage) +"&fanart="+quote_plus(fanart)+"&description="+quote_plus(description)+"&name2="+quote_plus(name2)+"&version="+quote_plus(version)
	ok=True
	liz=xbmcgui.ListItem(name)
	liz.setArt({'fanart':fanart,'icon':'DefaultFolder.png','thumb':iconimage})
	liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description,})
	if addcontext:
		contextMenu = []
		liz.addContextMenuItems(contextMenu)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)

def GetParams():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param

def get_mode():
	params=GetParams()
	mode = None
	try:
		mode=int(params["mode"])
	except:
		pass
	return mode

def Log(msg,msgtype):
	logit =False
	if msgtype =='debug' and setting_true('logging.debug'):
		logit = True
	elif msgtype == 'action' and setting_true('logging.actions'):
		logit = True
	elif msgtype == 'info' and setting_true('logging.info'):
		logit = True
	else:
		return
	if logit:
		fileinfo = getframeinfo(stack()[1][0])
		xbmc.log('*__{}__{}*{} Python file name = {} Line Number = {}'.format(addon_name,addon_version,msg,fileinfo.filename,fileinfo.lineno), level=xbmc.LOGINFO)
	else:pass