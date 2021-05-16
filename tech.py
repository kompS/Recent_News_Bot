import re
import os.path
import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse


class Tech:
    host = 'https://gadgets.ndtv.com'
    url = 'https://gadgets.ndtv.com/news'
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.259',
        'accept': '*/*'
    }

    newkey = ""
    lastkey_tech = ""
    lastkey_tech_file = ""

    def __init__(self, lastkey_tech_file):
        self.lastkey_tech_file = lastkey_tech_file

        if (os.path.exists(lastkey_tech_file)):
            self.lastkey_tech = open(lastkey_tech_file, 'r').read()
        else:
            f = open(lastkey_tech_file, 'w')
            self.lastkey_tech = self.get_lastkey_tech()
            f.write(self.lastkey_tech)
            f.close()

    def new_tech(self):
        r = requests.get(self.url,self.HEADERS)
        soup = BS(r.content, 'html.parser')

        new = ''
        items = soup.find('div', class_='caption_box').find('a').get('href')

        key = self.parse_href(items)
        if (self.lastkey_tech != key):
            new = key

        return new

    def tech_info(self):
        r = requests.get(self.url,self.HEADERS)
        soup = BS(r.content, 'html.parser')
        link = soup.find('div', class_='caption_box').find('a').get('href')

        postlink = link

        rr = requests.get(postlink)
        newsoup = BS(rr.content, 'html.parser')

        poster = newsoup.find('div', class_='fullstoryImage').find('img').get('src')

        info = {
            "title": soup.find('span', class_='news_listing').get_text(),
            "link": link,
            "image": poster,
            "text": newsoup.find('div', class_='content_text row description').find('p').get_text()
        }

        return info

    def download_image_tech(self, url):
        r = requests.get(url, allow_redirects=True)

        a = urlparse(url)
        filename = os.path.basename(a.path)
        open(filename, 'wb').write(r.content)

        return filename

    def get_lastkey_tech(self):
        r = requests.get(self.url)
        html = BS(r.content, 'html.parser')

        items = html.find('div', class_='caption_box').find('a').get('href')
        return self.parse_href(items)

    def parse_href(self, href):
        r = requests.get(self.url)
        html = BS(r.content, 'html.parser')

        result= html.find('div', class_='caption_box').find('a').get('href')
        self.newkey = result
        return result

    def update_lastkey_tech(self):
        self.lastkey_tech = self.newkey

        with open(self.lastkey_tech_file, "r+") as f:
            data = f.read()
            f.seek(0)
            f.write(str(self.newkey))
            f.truncate()
        return self.newkey
