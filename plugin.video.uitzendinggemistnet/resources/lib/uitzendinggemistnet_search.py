#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#
# Imports
#
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import object
import urllib.request, urllib.parse, urllib.error
import requests
import sys
import xbmc
import re
import os
import xbmcgui
import xbmcplugin

from resources.lib.uitzendinggemistnet_const import LANGUAGE, SETTINGS, convertToUnicodeString, log, getSoup, ADDON, IMAGES_PATH

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

        # Get plugin settings
        self.VIDEO = SETTINGS.getSetting('video')

        log("ARGV", repr(sys.argv))

        # Parse parameters...
        self.url = urllib.parse.parse_qs(urllib.parse.urlparse(sys.argv[2]).query)['url'][0]
        self.show_channel = urllib.parse.parse_qs(urllib.parse.urlparse(sys.argv[2]).query)['show_channel'][0]

        log("self.url", self.url)

        #
        # Play video...
        #
        self.search()

    #
    # Play video...
    #
    def search(self):
        #
        # Init
        #
        list_item = ''
        is_folder = False
        self.next_page_possible = False
        # Create a list for our items.
        listing = []

        dialog_wait = xbmcgui.DialogProgress()

        # https://www.uitzendinggemist.net/index.php?page=ajax&start=0&source=&what=spek
        # Get the search-string from the user
        keyboard = xbmc.Keyboard('', LANGUAGE(30004))
        keyboard.doModal()
        if keyboard.isConfirmed():
            self.search_string = keyboard.getText()
            self.url = self.url + self.search_string

        log("self.url", self.url)

        self.video_page_url = self.url

        # We still need to find out the video-url
        #
        # Get HTML page
        #
        try:
            response = requests.get(self.video_page_url)
        except urllib.error.HTTPError as error:

            log("first HTTPError", error)

            # Retry to (hopefully) get rid of a time-out http error
            try:
                response = requests.get(self.video_page_url)
            except urllib.error.HTTPError as error:

                log("second HTTPError", error)

                dialog_wait.close()
                del dialog_wait
                xbmcgui.Dialog().ok(LANGUAGE(30000), LANGUAGE(30507) % (str(error)))
                exit(1)

        html_source = response.text
        html_source = convertToUnicodeString(html_source)

        # Parse response
        soup = getSoup(html_source)

        # log("html_source", html_source)

        # <a "="" href="#" onclick="window.open('http://www.npo.nl/aa-aa/01-01-2015/AT_2119244','winname',...
        # items = soup.findAll('a', attrs={'onclick': re.compile("^" + "window")})

        items = soup.findAll('div', attrs={'class': re.compile("^" + "kr_blok_main")})

        log("len(items)", len(items))

        for item in items:

            item = convertToUnicodeString(item)

            log("item", item)

            video_page_url = item.a['href']

            log("video_page_url", video_page_url)

            #<div class="kr_blok_main" style="height: 320px;"><h3 class="kr_blok_title"><a href="https://www.uitzendinggemist.net/aflevering/500734/Ik_Vertrek.html" title="Ik Vertrek">Ik Vertrek</a></h3><div class="kr_blok_thumb"><a href="https://www.uitzendinggemist.net/aflevering/500734/Ik_Vertrek.html" title="Ik Vertrek - Milko En Mario In Portugal"><img src="https://images.poms.omroep.nl/image/s320/c320x180/1316596.jpg" alt="Ik Vertrek - Milko En Mario In Portugal" width="180" height="102"></a></div><p class="kr_blok_subtitle">Milko En Mario In Portugal</p><p class="kr_blok_desc">Mario (47) en Milko (54) wonen in een prachtig appartement in Amsterdam Oud-Zuid. De supermarkt is om de hoek, musea zijn op loopafstand en er is altijd leven op straat. Het ste ... </p><p class="kr_blok_date">03-01-2020</p><p class="kr_blok_host">TROS</p><p class="kr_blok_more"><a href="https://www.uitzendinggemist.net/programmas/328-Ik_Vertrek.html" title="Ik Vertrek Gemist">Alle afleveringen bekijken</a></p><p class="icon"><a href="https://www.uitzendinggemist.net/zenders/Nederland-2.html" title="Nederland 2"><img src="https://www.uitzendinggemist.net/images/nederland-2-xs.png" alt="Nederland 2" width="20" height="18" border="0"></a></p></div>

            #<div class="kr_blok_main" style="height: 270px;"><h3 class="kr_blok_title">Chateau Meiland </h3><div class="kr_blok_thumb"><a href="https://www.uitzendinggemist.net/programmas/59250-Chateau_Meiland.html"><img alt="Chateau Meiland " height="102" src="https://img.kijk.nl/media/cache/computer_retina_series_program_header/imgsrc06/images/redactioneel/1085720-LS---20190520112813--0e03ad5aaa47df615ea8e4d6f1204dbd.jpg" width="180"/></a></div><div class="kr_blok_desc">Martien en Erica gaan opnieuw het huwelijksbootje in</div><p class="icon"><a href="https://www.uitzendinggemist.net/zenders/SBS-6.html" title="SBS 6"><img alt="SBS 6" border="0" height="18" src="https://www.uitzendinggemist.net/images/sbs-6-xs.png" width="20"/></a></p></div>

            try:
                title_part1 = item.a['title']

                log("tp1", title_part1)

                title_part2 = item.img['alt']

                log("tp2", title_part2)

                title_part2 = convertToUnicodeString(title_part2)
                title_part2 = title_part2.replace(title_part1, '', 1)
                title_part2 = title_part2.replace(" -", "")
                title = title_part1 + ": " + title_part2
            except:
                try:
                    title = item.select('h3')[0].get_text(strip=True)
                except:
                    title = ""

            log("title", title)

            try:
                # Get the text of the second p-tag
                plot = item.select('p')[1].get_text(strip=True)
            except:
                try:
                    # Get the text of the second div-tag
                    plot = item.select('div')[1].get_text(strip=True)
                except:
                    plot = ""

            log("plot", plot)

            if title == "":
                pass
            else:
                title = title + " (" + plot + ")"

            log("title", title)

            if self.show_channel == "True":
                channel = item.select('img')[1]["alt"]

                log("channel", channel)

                channel = str(channel).replace("Nederland", "NL ")

                title = channel + ": " + title

            thumbnail_url = item.img['src']

            log("thumbnail_url", thumbnail_url)

            # Add to list...
            list_item = xbmcgui.ListItem(title)
            list_item.setInfo("video", {"title": title, "studio": ADDON, "mediatype": "video",
                              "plot": plot})
            list_item.setArt({'thumb': thumbnail_url, 'icon': thumbnail_url,
                              'fanart': os.path.join(IMAGES_PATH, 'fanart-blur.jpg')})
            list_item.setProperty('IsPlayable', 'true')

            # let's remove any non-ascii characters
            title = title.encode('ascii', 'ignore')

            parameters = {"action": "play-episode", "video_page_url": video_page_url, "title": title}
            url = self.plugin_url + '?' + urllib.parse.urlencode(parameters)
            is_folder = False
            # Add refresh option to context menu
            list_item.addContextMenuItems([('Refresh', 'Container.Refresh')])
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
