# -*- coding: utf-8 -*-
import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys,xbmcvfs
import shutil
import urllib

import re

addon_id = 'plugin.ghostclose.kodi'
ADDON = xbmcaddon.Addon(id=addon_id)
FANART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
ART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
VERSION = "3.0.0"
PATH = "forceclose"            
BASE = "fclose"
DIALOG         = xbmcgui.Dialog()
COLOR1         = 'red'
COLOR2         = 'white'
log            = xbmc.translatePath('special://logpath/')

KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split('.', 1)[0])
if KODI_VERSION<=18:
    que=urllib.quote_plus
    url_encode=urllib.urlencode
    unque=urllib.unquote_plus
else:
    import urllib.parse
    que=urllib.parse.quote_plus
    url_encode=urllib.parse.urlencode
    unque=urllib.parse.unquote_plus
###################################
####KILL XBMC Flawless Force Close#
###################################
#
def flawless():
    choice = DIALOG.yesno('Kodi afsluiten', '[COLOR %s]U staat op het punt om Kodi af te sluiten' % COLOR2, 'Doorgaan?[/COLOR]', nolabel='[B][COLOR red] Nee[/COLOR][/B]',yeslabel='[B][COLOR green]Ja[/COLOR][/B]')
	if choice == 1:
		os._exit(1)
	else:
		xbmc.executebuiltin("Action(Close)")
#############################

#############################
########Old Method###########
#############################
def oldmeth():
    dialog = xbmcgui.Dialog()
    choice = 1
    choice = DIALOG.yesno('Kodi afsluiten', '[COLOR %s]U staat op het punt om Kodi af te sluiten' % COLOR2, 'Doorgaan?[/COLOR]', nolabel='[B][COLOR red] Nee[/COLOR][/B]',yeslabel='[B][COLOR green]Ja[/COLOR][/B]')
    if choice == 0:
        xbmc.executebuiltin("Action(Close)")
        return
    elif choice == 1:
        pass
    log_path = xbmc.translatePath('special://logpath')
    if xbmc.getCondVisibility('system.platform.android'):
        try: os.system('kill $(ps | busybox grep org.xbmc.kodi | busybox awk "{ print $2 }")')
        except: pass
        try: os.system('kill $(ps | busybox grep com.sempermax.spmc16 | busybox awk "{ print $2 }")')
        except: pass
        try: os.system('kill $(ps | busybox grep com.sempermax.spmc | busybox awk "{ print $2 }")')
        except: pass
        try: os.system('kill $(ps | busybox grep org.xbmc.kodi | busybox awk "{ print $2 }")')
        except: pass             
        #

    if xbmc.getCondVisibility('system.platform.linux'):
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall SMC')
        except: pass
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 SMC.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        #

    if xbmc.getCondVisibility('system.platform.osx'):
        try: os.system('killall -9 Kodi')
        except: pass
        try: os.system('killall -9 SMC')
        except: pass
        try: os.system('killall -9 XBMC')
        except: pass
        #

    if xbmc.getCondVisibility('system.platform.atv2'):
        try: os.system('killall AppleTV')
        except: pass
        #
        
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        try: os.system('sudo initctl stop tvmc')
        except: pass
        try: os.system('sudo initctl stop smc')
        except: pass
        #
    else:
        
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        try: os.system('sudo initctl stop tvmc')
        except: pass
        try: os.system('sudo initctl stop smc')
        except: pass

        #
    #dialog.ok("WARNING", "Force Close was unsuccessful.","Closing Kodi normally...",'')
    #xbmc.executebuiltin('Quit')
    xbmc.executebuiltin('ActivateWindow(ShutdownMenu)')

def omfci():
    if xbmc.getCondVisibility('system.platform.android'):
        try: os.system('kill $(ps | busybox grep org.xbmc.kodi | busybox awk "{ print $2 }")')
        except: pass
        try: os.system('kill $(ps | busybox grep com.sempermax.spmc16 | busybox awk "{ print $2 }")')
        except: pass
        try: os.system('kill $(ps | busybox grep com.sempermax.spmc | busybox awk "{ print $2 }")')
        except: pass
        try: os.system('kill $(ps | busybox grep org.xbmc.kodi | busybox awk "{ print $2 }")')
        except: pass             
        #

    if xbmc.getCondVisibility('system.platform.linux'):
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall SMC')
        except: pass
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 SMC.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        #

    if xbmc.getCondVisibility('system.platform.osx'):
        try: os.system('killall -9 Kodi')
        except: pass
        try: os.system('killall -9 SMC')
        except: pass
        try: os.system('killall -9 XBMC')
        except: pass
        #
 
    if xbmc.getCondVisibility('system.platform.atv2'):
        try: os.system('killall AppleTV')
        except: pass
        #
        
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        try: os.system('sudo initctl stop tvmc')
        except: pass
        try: os.system('sudo initctl stop smc')
        except: pass
        #
    else:
        
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        try: os.system('sudo initctl stop tvmc')
        except: pass
        try: os.system('sudo initctl stop smc')
        except: pass

        #
    #dialog.ok("WARNING", "Force Close was unsuccessful.","Closing Kodi normally...",'')
    #xbmc.executebuiltin('Quit')
    xbmc.executebuiltin('ActivateWindow(ShutdownMenu)')
    #
def INDEX():
	addDir('Systeem afsluiten (Aanbevolen)',BASE,10,ART+'force.png',FANART,'')
	addDir('Geforceerd afsluiten om af te sluiten',BASE,4,ART+'force.png',FANART,'')
	addDir('Normale methode',BASE,736641,ART+'force.png',FANART,'')
	addDir('Op de oude manier geforceerd afsluiten',BASE,736642,ART+'force.png',FANART,'')
def get_params():
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
		
        

    

def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+que(url)+"&mode="+str(mode)+"&name="+que(name)+"&iconimage="+que(iconimage)+"&fanart="+que(fanart)+"&description="+que(description)
        ok=True
        if KODI_VERSION<=18:
            liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        else:
            liz=xbmcgui.ListItem(name)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        if mode==90 :
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

        
                      
params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None
description=None

#######################################    ^
# Manual Mode Old Method (For Pussies)#    |
#######################################    |


##########################################
	
try:
        url=unque(params["url"])
except:
        pass
try:
        name=unque(params["name"])
except:
        pass
try:
        iconimage=unque(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=unque(params["fanart"])
except:
        pass
try:        
        description=unque(params["description"])
except:
        pass
        
        



def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )
        
        
if mode==None or url==None or len(url)<1:
        INDEX()

elif mode==10:
        flawless()

elif mode==4:
        os._exit(1)
		
elif mode==736641:
        oldmeth()

elif mode==736642:
        omfci()		

xbmcplugin.endOfDirectory(int(sys.argv[1]))
