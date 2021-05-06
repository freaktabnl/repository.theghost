import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os


ADDON = xbmcaddon.Addon(id='plugin.video.ghostadult')
DATA_PATH = os.path.join(xbmc.translatePath('special://profile/data/plugin.video.ghostadult'), '')

def addon():
    return ADDON

def setView():
    if ADDON.getSetting('auto-view') == 'true':
        return True
    else:
        return False

        
        
