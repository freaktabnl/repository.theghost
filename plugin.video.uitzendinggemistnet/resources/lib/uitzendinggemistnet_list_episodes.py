#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#
# Imports
#
from future import standard_library
standard_library.install_aliases()
from builtins import str
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

        # Parse parameters
        # try:
        self.plugin_category = urllib.parse.parse_qs(urllib.parse.urlparse(sys.argv[2]).query)['plugin_category'][0]
        self.video_list_page_url = urllib.parse.parse_qs(urllib.parse.urlparse(sys.argv[2]).query)['url'][0]
        self.next_page_possible = urllib.parse.parse_qs(urllib.parse.urlparse(sys.argv[2]).query)['next_page_possible'][0]
        self.show_channel = urllib.parse.parse_qs(urllib.parse.urlparse(sys.argv[2]).query)['show_channel'][0]
        # except KeyError:
        #     self.plugin_category = LANGUAGE(30001)
        #     self.video_list_page_url = "http://uitzendinggemist.net/"
        #     self.next_page_possible = "False"
        #     self.show_channel = "False"

        log("self.video_list_page_url", self.video_list_page_url)

        # if self.next_page_possible == 'True':
        #     # Determine current page number and base_url
        #     # find last slash
        #     pos_of_last_slash = self.video_list_page_url.rfind('/')
        #     # remove last slash
        #     self.video_list_page_url = self.video_list_page_url[0: pos_of_last_slash]
        #     pos_of_last_slash = self.video_list_page_url.rfind('/')
        #     self.base_url = self.video_list_page_url[0: pos_of_last_slash + 1]
        #     self.current_page = self.video_list_page_url[pos_of_last_slash + 1:]
        #     self.current_page = int(self.current_page)
        #     # add last slash
        #     self.video_list_page_url = str(self.video_list_page_url) + "/"
        #
        #     log("self.base_url", self.base_url)

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
        # Create a list for our items.
        listing = []

        #
        # Get HTML page
        #
        response = requests.get(self.video_list_page_url)

        html_source = response.text
        html_source = convertToUnicodeString(html_source)

        # Parse response
        soup = getSoup(html_source)

        # <div class="kr_blok_main" style="height: 320px;"><h3 class="kr_blok_title"><a href="https://www.uitzendinggemist.net/aflevering/500114/Ik_Vertrek.html" title="Ik Vertrek">Ik Vertrek</a></h3><div class="kr_blok_thumb"><a href="https://www.uitzendinggemist.net/aflevering/500114/Ik_Vertrek.html" title="Ik Vertrek - Marjon En Vincent - Tsjechië"><img src="https://images.poms.omroep.nl/image/s320/c320x180/1312993.jpg" alt="Ik Vertrek - Marjon En Vincent - Tsjechië" width="180" height="102"></a></div><p class="kr_blok_subtitle">Marjon En Vincent - Tsjechië</p><p class="kr_blok_desc">Dierenwinkelmedewerkster Marjon (32) heeft de droom om met haar eigen beestenboel op het platteland van Tsjechië te wonen. Haar vriend Vincent (37) is nog niet overtuigd. H ... </p><p class="kr_blok_date">28-12-2019</p><p class="kr_blok_host">TROS</p><p class="kr_blok_more"><a href="https://www.uitzendinggemist.net/programmas/328-Ik_Vertrek.html" title="Ik Vertrek Gemist">Alle afleveringen bekijken</a></p><p class="icon"><a href="https://www.uitzendinggemist.net/zenders/Nederland-2.html" title="Nederland 2"><img src="https://www.uitzendinggemist.net/images/nederland-2-xs.png" alt="Nederland 2" width="20" height="18" border="0"></a></p></div>

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

            if self.show_channel == "True":
                channel = item.select('img')[1]["alt"]

                log("channel", channel)

                channel = str(channel).replace("Nederland", "NL ")

                title = channel + ": " + title

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

            thumbnail_url = item.img['src']

            log("thumbnail_url", thumbnail_url)

            context_menu_items = []
            # Add refresh option to context menu
            context_menu_items.append((LANGUAGE(30667), 'Container.Refresh'))

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
