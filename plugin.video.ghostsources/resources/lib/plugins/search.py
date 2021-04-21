from bs4 import BeautifulSoup
import requests
import re
from ..plugin import Plugin
import xbmcgui

class Search(Plugin):
    name = "search"
    
    def get_list(self, url):
        if not url.startswith("search"):
            return False
        results = []
        url = "https://textbin.net/raw/g4s4melbbp"
        page = requests.get(url)

        soup = BeautifulSoup(page.text, "html.parser")

        dialog = xbmcgui.Dialog()
        d = dialog.input('Vul uw zoekwoord in en klik op OK', type=xbmcgui.INPUT_ALPHANUM)
        for item in soup.find_all('item'):
            title = item.title.text
            summary = item.summary.text
            links = re.findall(r"(https?://.*?)(?:\s|$)", str(summary))
            if not links:
                continue
            if title == 'Meerdere bronnen tegelijk toevoegen':
                continue
            if d.lower() in title.lower():
                results.append(str(item))
        if results:
        	return f'<xml>{"".join(results)}</xml>'
        else:
        	return "<xml><item><title>Geen bron gevonden helaas.</title><link></link></item></xml>"
