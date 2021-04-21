#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#
# Imports
#
from future import standard_library
standard_library.install_aliases()
from builtins import object
import sys
import urllib.request, urllib.parse, urllib.error
import xbmcgui
import xbmcplugin
import os

from resources.lib.uitzendinggemistnet_const import LANGUAGE, IMAGES_PATH


#
# Main class
#
class Main(object):
    def __init__(self):
        # Get the command line arguments
        # Get the plugin url in plugin:// notation
        self.plugin_url = sys.argv[0]
        # Get the plugin handle as an integer number
        self.plugin_handle = int(sys.argv[1])

        #
        # uitzendinggemistnet Rtl-4
        #
        parameters = {"action": "list-tv-shows", "plugin_category": LANGUAGE(30014),
                      "url": "https://www.uitzendinggemist.net/zenders/RTL-4.html", "next_page_possible": "False",
                      "show_channel": "False"}
        url = self.plugin_url + '?' + urllib.parse.urlencode(parameters)
        list_item = xbmcgui.ListItem(LANGUAGE(30014))
        list_item.setArt({'thumb': 'DefaultFolder.png', 'icon': 'DefaultFolder.png',
                          'fanart': os.path.join(IMAGES_PATH, 'fanart-blur.jpg')})
        is_folder = True
        list_item.setProperty('IsPlayable', 'false')
        xbmcplugin.addDirectoryItem(handle=self.plugin_handle, url=url, listitem=list_item, isFolder=is_folder)

        #
        # uitzendinggemistnet Rtl-5
        #
        parameters = {"action": "list-tv-shows", "plugin_category": LANGUAGE(30015),
                      "url": "https://www.uitzendinggemist.net/zenders/RTL-5.html", "next_page_possible": "False",
                      "show_channel": "False"}
        url = self.plugin_url + '?' + urllib.parse.urlencode(parameters)
        list_item = xbmcgui.ListItem(LANGUAGE(30015))
        list_item.setArt({'thumb': 'DefaultFolder.png', 'icon': 'DefaultFolder.png',
                          'fanart': os.path.join(IMAGES_PATH, 'fanart-blur.jpg')})
        is_folder = True
        list_item.setProperty('IsPlayable', 'false')
        xbmcplugin.addDirectoryItem(handle=self.plugin_handle, url=url, listitem=list_item, isFolder=is_folder)

        #
        # uitzendinggemistnet Rtl-7
        #
        parameters = {"action": "list-tv-shows", "plugin_category": LANGUAGE(30017),
                      "url": "https://www.uitzendinggemist.net/zenders/RTL-7.html", "next_page_possible": "False",
                      "show_channel": "False"}
        url = self.plugin_url + '?' + urllib.parse.urlencode(parameters)
        list_item = xbmcgui.ListItem(LANGUAGE(30017))
        list_item.setArt({'thumb': 'DefaultFolder.png', 'icon': 'DefaultFolder.png',
                          'fanart': os.path.join(IMAGES_PATH, 'fanart-blur.jpg')})
        is_folder = True
        list_item.setProperty('IsPlayable', 'false')
        xbmcplugin.addDirectoryItem(handle=self.plugin_handle, url=url, listitem=list_item, isFolder=is_folder)

        #
        # uitzendinggemistnet Rtl-8
        #
        parameters = {"action": "list-tv-shows", "plugin_category": LANGUAGE(30018),
                      "url": "https://www.uitzendinggemist.net/zenders/RTL-8.html", "next_page_possible": "False",
                      "show_channel": "False"}
        url = self.plugin_url + '?' + urllib.parse.urlencode(parameters)
        list_item = xbmcgui.ListItem(LANGUAGE(30018))
        list_item.setArt({'thumb': 'DefaultFolder.png', 'icon': 'DefaultFolder.png',
                          'fanart': os.path.join(IMAGES_PATH, 'fanart-blur.jpg')})
        is_folder = True
        list_item.setProperty('IsPlayable', 'false')
        xbmcplugin.addDirectoryItem(handle=self.plugin_handle, url=url, listitem=list_item, isFolder=is_folder)

        #
        # Search
        #
        parameters = {"action": "search", "plugin_category": LANGUAGE(30004),
                      "url": "https://www.uitzendinggemist.net/index.php?page=ajax&start=0&source=&what=",
                      "next_page_possible": "False", "show_channel": "True"}
        url = self.plugin_url + '?' + urllib.parse.urlencode(parameters)
        list_item = xbmcgui.ListItem(LANGUAGE(30004))
        list_item.setArt({'thumb': 'DefaultFolder.png', 'icon': 'DefaultFolder.png',
                          'fanart': os.path.join(IMAGES_PATH, 'fanart-blur.jpg')})
        is_folder = True
        list_item.setProperty('IsPlayable', 'false')
        xbmcplugin.addDirectoryItem(handle=self.plugin_handle, url=url, listitem=list_item, isFolder=is_folder)

        #
        # uitzendinggemistnet all tv shows
        #
        parameters = {"action": "list-tv-shows-all", "plugin_category": LANGUAGE(30005),
                      "url": "https://www.uitzendinggemist.net/programmas/",
                      "next_page_possible": "False", "show_channel": "False"}
        url = self.plugin_url + '?' + urllib.parse.urlencode(parameters)
        list_item = xbmcgui.ListItem(LANGUAGE(30005))
        list_item.setArt({'thumb': 'DefaultFolder.png', 'icon': 'DefaultFolder.png',
                          'fanart': os.path.join(IMAGES_PATH, 'fanart-blur.jpg')})
        is_folder = True
        list_item.setProperty('IsPlayable', 'false')
        xbmcplugin.addDirectoryItem(handle=self.plugin_handle, url=url, listitem=list_item, isFolder=is_folder)

        #
        # uitzendinggemistnet latest videos
        #
        parameters = {"action": "list-episodes", "plugin_category": LANGUAGE(30001),
                      "url": "https://www.uitzendinggemist.net", "next_page_possible": "False",
                      "show_channel": "True"}
        url = self.plugin_url + '?' + urllib.parse.urlencode(parameters)
        list_item = xbmcgui.ListItem(LANGUAGE(30001))
        list_item.setArt({'thumb': 'DefaultFolder.png', 'icon': 'DefaultFolder.png',
                          'fanart': os.path.join(IMAGES_PATH, 'fanart-blur.jpg')})
        is_folder = True
        list_item.setProperty('IsPlayable', 'false')
        xbmcplugin.addDirectoryItem(handle=self.plugin_handle, url=url, listitem=list_item, isFolder=is_folder)

        #
        # uitzendinggemistnet popular videos
        #
        parameters = {"action": "list-tv-shows", "plugin_category": LANGUAGE(30002),
                      "url": "https://www.uitzendinggemist.net/programmas/populair/", "next_page_possible": "False",
                      "show_channel": "True"}
        url = self.plugin_url + '?' + urllib.parse.urlencode(parameters)
        list_item = xbmcgui.ListItem(LANGUAGE(30002))
        list_item.setArt({'thumb': 'DefaultFolder.png', 'icon': 'DefaultFolder.png',
                          'fanart': os.path.join(IMAGES_PATH, 'fanart-blur.jpg')})
        is_folder = True
        list_item.setProperty('IsPlayable', 'false')
        xbmcplugin.addDirectoryItem(handle=self.plugin_handle, url=url, listitem=list_item, isFolder=is_folder)

        # Disable sorting
        xbmcplugin.addSortMethod(handle=self.plugin_handle, sortMethod=xbmcplugin.SORT_METHOD_NONE)
        # Finish creating a virtual folder.
        xbmcplugin.endOfDirectory(self.plugin_handle)
