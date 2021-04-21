#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#
# Imports
#
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import range
from builtins import object
import os
import re
import requests
import sys
import urllib.request, urllib.parse, urllib.error
import xbmcgui
import xbmcplugin

from resources.lib.uitzendinggemistnet_const import LANGUAGE, IMAGES_PATH, ADDON, convertToUnicodeString, log, getSoup


#
# Main class
#
class Main(object):
    #
    # Init
    #
    def __init__(self):
        # Get the command line arguments
        # Get the plugin url in plugin:// notation
        self.plugin_url = sys.argv[0]
        # Get the plugin handle as an integer number
        self.plugin_handle = int(sys.argv[1])

        log("ARGV", repr(sys.argv))

        # Parse parameters...
        self.plugin_category = urllib.parse.parse_qs(urllib.parse.urlparse(sys.argv[2]).query)['plugin_category'][0]
        self.video_list_page_url = urllib.parse.parse_qs(urllib.parse.urlparse(sys.argv[2]).query)['url'][0]
        self.next_page_possible = urllib.parse.parse_qs(urllib.parse.urlparse(sys.argv[2]).query)['next_page_possible'][0]
        self.show_channel = urllib.parse.parse_qs(urllib.parse.urlparse(sys.argv[2]).query)['show_channel'][0]

        log("self.video_list_page_url", self.video_list_page_url)

        # # Determine base_url
        # # find last slash
        # pos_of_last_slash = self.video_list_page_url.rfind('/')
        # # remove last slash
        # self.video_list_page_url = self.video_list_page_url[0: pos_of_last_slash]
        # pos_of_last_slash = self.video_list_page_url.rfind('/')
        # self.base_url = self.video_list_page_url[0: pos_of_last_slash + 1]
        # # add last slash
        # self.video_list_page_url = str(self.video_list_page_url) + "/"
        #
        # log("self.base_url", self.base_url)

        #
        # Get the videos...
        #
        self.getVideos()

    #
    # Get videos...
    #
    def getVideos(self):
        #
        # Init
        #
        current_page = 1
        # title = ""
        thumbnail_url = ""
        list_item = ''
        is_folder = False
        # Create a list for our items.
        listing = []

        #
        # Get HTML page
        #
        response = requests.get(self.video_list_page_url)

        html_source = response.text
        html_source = convertToUnicodeString(html_source)

        # log("html_source", html_source)

        # Parse response
        soup = getSoup(html_source)

        #<a href="https://www.uitzendinggemist.net/programmas/5339-1_April_Met_Jack_De_Aap.html" title="1 April Met Jack De Aap">1 April Met Jack De Aap</a>
        tv_shows = soup.findAll('a', attrs={'href': re.compile("^https://www.uitzendinggemist.net/programmas/")})

        for tv_show in tv_shows:

            log("tv_show", tv_show)

            video_page_url = tv_show['href']

            log("video_page_url", video_page_url)

            last_part_of_video_url = str(video_page_url).replace("https://www.uitzendinggemist.net/programmas/", "")

            log("last_part_of_video_url", last_part_of_video_url)

            if last_part_of_video_url == "":

                log("skipping video_page_url with empty last_part_of_video_url after https://www.uitzendinggemist.net/programmas/ in url", video_page_url)

                continue

            letter_or_number = last_part_of_video_url[0:1]
            slash_or_no_slash = last_part_of_video_url[1:2]

            if letter_or_number.isalpha():

                log("skipping video_page_url with letter after https://www.uitzendinggemist.net/programmas/ in url", video_page_url)

                continue

            if slash_or_no_slash == "/":

                log("skipping video_page_url with slash after number after https://www.uitzendinggemist.net/programmas/ in url", video_page_url)

                continue

            title = tv_show["title"]

            if self.show_channel == "True":
                channel = tv_show.select('img')[1]["alt"]

                log("channel", channel)

                channel = str(channel).replace("Nederland", "NL ")

                title = channel + ": " + title

            log("title", title)

            context_menu_items = []
            # Add refresh option to context menu
            context_menu_items.append((LANGUAGE(30667), 'Container.Refresh'))

            # Add to list...
            list_item = xbmcgui.ListItem(title)
            list_item.setArt({'thumb': thumbnail_url, 'icon': thumbnail_url,
                              'fanart': os.path.join(IMAGES_PATH, 'fanart-blur.jpg')})
            list_item.setProperty('IsPlayable', 'false')

            # let's remove any non-ascii characters
            title = title.encode('ascii', 'ignore')

            parameters = {"action": "list-episodes", "plugin_category": title, "url": video_page_url,
                          "next_page_possible": "False", "show_channel": "True", "title": title}
            url = self.plugin_url + '?' + urllib.parse.urlencode(parameters)
            is_folder = True
            # Adding context menu items to context menu
            list_item.addContextMenuItems(context_menu_items, replaceItems=False)
            # Add our item to the listing as a 3-element tuple.
            listing.append((url, list_item, is_folder))

        # # Next page entry
        # if self.next_page_possible == 'True':
        #     thumbnail_url = os.path.join(IMAGES_PATH, 'next-page.png')
        #     list_item = xbmcgui.ListItem(LANGUAGE(30503))
        #     list_item.setArt({'thumb': thumbnail_url, 'icon': thumbnail_url,
        #                       'fanart': os.path.join(IMAGES_PATH, 'fanart-blur.jpg')})
        #     list_item.setProperty('IsPlayable', 'false')
        #     parameters = {"action": "list", "plugin_category": self.plugin_category, "url": str(self.next_url),
        #                   "next_page_possible": self.next_page_possible}
        #     url = self.plugin_url + '?' + urllib.parse.urlencode(parameters)
        #     is_folder = True
        #     # Add refresh option to context menu
        #     list_item.addContextMenuItems([('Refresh', 'Container.Refresh')])
        #     # Add our item to the listing as a 3-element tuple.
        #     listing.append((url, list_item, is_folder))
        #
        #     log("next url", url)

        # Add our listing to Kodi.
        # Large lists and/or slower systems benefit from adding all items at once via addDirectoryItems
        # instead of adding one by ove via addDirectoryItem.
        xbmcplugin.addDirectoryItems(self.plugin_handle, listing, len(listing))
        # Disable sorting
        xbmcplugin.addSortMethod(handle=self.plugin_handle, sortMethod=xbmcplugin.SORT_METHOD_NONE)
        # Finish creating a virtual folder.
        xbmcplugin.endOfDirectory(self.plugin_handle)
