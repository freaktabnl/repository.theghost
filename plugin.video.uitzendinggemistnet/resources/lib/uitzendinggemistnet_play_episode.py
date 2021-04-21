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
import re
import json
import xbmcgui
import xbmcplugin

from resources.lib.uitzendinggemistnet_const import LANGUAGE, SETTINGS, convertToUnicodeString, log, getSoup

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
        self.video_page_url = urllib.parse.parse_qs(urllib.parse.urlparse(sys.argv[2]).query)['video_page_url'][0]
        # Get the title.
        self.title = urllib.parse.parse_qs(urllib.parse.urlparse(sys.argv[2]).query)['title'][0]
        self.title = str(self.title)

        log("self.video_page_url", self.video_page_url)

        #
        # Play video...
        #
        self.playVideo()

    #
    # Play video...
    #
    def playVideo(self):
        #
        # Init
        #
        no_url_found = False
        unplayable_media_file = False
        have_valid_url = False
        video_unavailable = False

        dialog_wait = xbmcgui.DialogProgress()

        #
        # Get current list item details...
        #
        # title = convertToUnicodeString(xbmc.getInfoLabel("list_item.Title"))
        # thumbnail_url = convertToUnicodeString(xbmc.getInfoImage("list_item.Thumb"))
        # studio = convertToUnicodeString(xbmc.getInfoLabel("list_item.Studio"))
        # plot = convertToUnicodeString(xbmc.getInfoLabel("list_item.Plot"))
        # genre = convertToUnicodeString(xbmc.getInfoLabel("list_item.Genre"))

        stream_video_url = ''

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
        items = soup.findAll('a', attrs={'onclick': re.compile("^" + "window")})

        log("len(items)", len(items))

        for item in items:

            # log('item', item)

            item = convertToUnicodeString(item)

            start_pos_url = str(item).find("http")
            end_pos_url = str(item).find("'", start_pos_url)
            url = str(item)[start_pos_url: end_pos_url]

            # log("url", url)

            pos_last_slash = url.rfind("/")
            api_url_middle_part = url[pos_last_slash + 1:]

            # log("aump:", api_url_middle_part)

            # https://api.rtl.nl/watch/play/api/play/xl/9ed0c3a7-b43c-3dad-9099-8c7ab3f7e938?device=web&format=hls
            api_url = "https://api.rtl.nl/watch/play/api/play/xl/" + api_url_middle_part + "?device=web&format=hls"

            #
            # Get HTML page
            #
            try:
                response = requests.get(api_url)
            except urllib.error.HTTPError as error:

                log("first HTTPError", error)

            json_source = response.text
            json_source = convertToUnicodeString(json_source)

            log("json_source", json_source)

            #{"canPlay":true,"manifest":"https://cdn-rtlvod-h4.akamaized.net/d126579c-7897-4396-bf0d-e9913da04cf9/4cf1064e-7c33-33c5-a6d4-9baea9f515c7.ism/manifest(format=m3u8-aapl,encryption=cbc,Filter=Quality)","token":"eyJhbGciOiJSUzI1NiIsImtpZCI6IkRGMUEwNzYwODRFRTE4NDM5NTYwMjdCM0UxODIxMkZBRTA0OUM3NTgiLCJ0eXAiOiJKV1QifQ.eyJ1dWlkIjoiNGNmMTA2NGUtN2MzMy0zM2M1LWE2ZDQtOWJhZWE5ZjUxNWM3IiwidGVuYW50IjoiWGwiLCJuYmYiOjE1NzgwNzI2MzYsImV4cCI6MTU3ODA3NjIzNiwiaWF0IjoxNTc4MDcyNjM2LCJpc3MiOiJodHRwczovL2VudGl0bGVtZW50LnJ0bC5ubCIsImF1ZCI6IlJUTCJ9.OzRTzM7kfCYcU-nIe8L3uzeDnYfJFKog8gmlQh3IUmqoxxY5pcjG8lZe_HloxJJBTRbQDAhFG3f6yiwDzCg_bLYY0QvpiS_gpsKBaTyVZ9KxMi7mq5vcD1eGAL6jaOXNzmrm68zJ0ufNlPZ5dAzIcYABWfLqBH9C-iVr8lHAW6jfrtHqRvIV3r2-lezI5_qhxNThR6NyEjO7WvRdTqdBbMpa7_eVLTpvzFdtc-UKrRNViPPaTAKwMHEssjYkjwEvBkvoSRQZy-P9ahqq4B5KGo9x03kIUFXd5XgbMT4rMli_hTmRQDFBrt5Mo5JRApVp1x7BgiAJqAFvQk0zDvWnsA","kid":"1e444b87-1beb-431e-ae3c-4463bdbf2dcd","licenseUrl":"https://api.rtl.nl/watch/license/aes/?kid=1e444b87-1beb-431e-ae3c-4463bdbf2dcd"}

            data = json.loads(json_source)

            # can_play = data["canPlay"]
            #
            # log("can_play", can_play)

            manifest_url = data["manifest"]

            # log("manifest_url", manifest_url)

            have_valid_url = True
            unplayable_media_file = False
            video_url = manifest_url

            # if can_play:
            #     have_valid_url = True
            #     unplayable_media_file = False
            #     video_url = manifest_url
            # else:
            #
            #     log("skipping video that cannot be played", manifest_url)
            #
            #     have_valid_url = False
            #     video_unavailable = True
            #     video_url = ""

        log("have_valid_url", have_valid_url)

        log("video_url", video_url)

        if have_valid_url:
            list_item = xbmcgui.ListItem(path=video_url)
            xbmcplugin.setResolvedUrl(self.plugin_handle, True, list_item)

        #
        # Alert user
        #
        elif no_url_found:
            xbmcgui.Dialog().ok(LANGUAGE(30000), LANGUAGE(30505))
        elif unplayable_media_file:
            xbmcgui.Dialog().ok(LANGUAGE(30000), LANGUAGE(30506))
        elif video_unavailable:
            xbmcgui.Dialog().ok(LANGUAGE(30000), LANGUAGE(30666))