import xbmcaddon

import os

#########################################################
#         Global Variables - DON'T EDIT!!!              #
#########################################################
ADDON_ID = xbmcaddon.Addon().getAddonInfo('id')
PATH = xbmcaddon.Addon().getAddonInfo('path')
ART = os.path.join(PATH, 'resources', 'media')
#########################################################

#########################################################
#        User Edit Variables                            #
#########################################################
ADDONTITLE = '[COLOR limegreen][B]Open[/B][/COLOR]Wizard'
BUILDERNAME = 'OpenWizard'
EXCLUDES = [ADDON_ID, 'repository.openwizard']
BUILDFILE = 'https://pastebin.com/raw/EkvT2ENx'
UPDATECHECK = 0
APKFILE = 'http://'
YOUTUBETITLE = ''
YOUTUBEFILE = 'http://'
ADDONFILE = 'http://'
ADVANCEDFILE = 'http://'
#########################################################

#########################################################
#        Theming Menu Items                             #
#########################################################
ICONBUILDS = os.path.join(ART, 'builds.png')
ICONMAINT = os.path.join(ART, 'maintenance.png')
ICONSPEED = os.path.join(ART, 'speed.png')
ICONAPK = os.path.join(ART, 'apkinstaller.png')
ICONADDONS = os.path.join(ART, 'addoninstaller.png')
ICONYOUTUBE = os.path.join(ART, 'youtube.png')
ICONSAVE = os.path.join(ART, 'savedata.png')
ICONTRAKT = os.path.join(ART, 'keeptrakt.png')
ICONREAL = os.path.join(ART, 'keepdebrid.png')
ICONLOGIN = os.path.join(ART, 'keeplogin.png')
ICONCONTACT = os.path.join(ART, 'information.png')
ICONSETTINGS = os.path.join(ART, 'settings.png')
HIDESPACERS = 'No'
SPACER = '='

COLOR1 = 'limegreen'
COLOR2 = 'white'
# Primary menu items   / {0} is the menu item and is required
THEME1 = u'[COLOR {color1}][I]([COLOR {color1}][B]Open[/B][/COLOR][COLOR {color2}]Wizard[COLOR {color1}])[/I][/COLOR] [COLOR {color2}]{{}}[/COLOR]'.format(color1=COLOR1, color2=COLOR2)
# Build Names          / {0} is the menu item and is required
THEME2 = u'[COLOR {color1}]{{}}[/COLOR]'.format(color1=COLOR1)
# Alternate items      / {0} is the menu item and is required
THEME3 = u'[COLOR {color1}]{{}}[/COLOR]'.format(color1=COLOR1)
# Current Build Header / {0} is the menu item and is required
THEME4 = u'[COLOR {color1}]Current Build:[/COLOR] [COLOR {color2}]{{}}[/COLOR]'.format(color1=COLOR1, color2=COLOR2)
# Current Theme Header / {0} is the menu item and is required
THEME5 = u'[COLOR {color1}]Current Theme:[/COLOR] [COLOR {color2}]{{}}[/COLOR]'.format(color1=COLOR1, color2=COLOR2)

HIDECONTACT = 'Yes'
CONTACT = 'Thank you for choosing OpenWizard.'
CONTACTICON = os.path.join(ART, 'qricon.png')
CONTACTFANART = 'http://'
#########################################################

#########################################################
#        Auto Update For Those With No Repo             #
#########################################################
AUTOUPDATE = 'No'
#########################################################

#########################################################
#        Auto Install Repo If Not Installed             #
#########################################################
AUTOINSTALL = 'No'
REPOID = 'repository.theghost'
REPOADDONXML = 'https://'
REPOZIPURL = 'https://'
#########################################################

#########################################################
#        Notification Window                            #
#########################################################
ENABLE = 'No'
NOTIFICATION = 'http://'
HEADERTYPE = 'Text'
FONTHEADER = 'Font14'
HEADERMESSAGE = '[COLOR limegreen][B]Open[/B][/COLOR]Wizard'
HEADERIMAGE = 'http://'
FONTSETTINGS = 'Font13'
BACKGROUND = 'http://'
#########################################################
