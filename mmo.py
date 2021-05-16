import re
import os.path
import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse


class Mmo:
    url = 'https://www.goha.ru/mmorpg'
    host = 'https://www.goha.ru/'
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.259','accept': '*/*'}


    newkey = ""
    lastkey_mmo = ""
    lastkey_mmo_file = ""

    def __init__(self, lastkey_mmo_file):
        self.lastkey_mmo_file = lastkey_mmo_file

        if (os.path.exists(lastkey_mmo_file)):
            self.lastkey_mmo = open(lastkey_mmo_file, 'r').read()
        else:
            f = open(lastkey_mmo_file, 'w')
            self.lastkey_mmo = self.get_lastkey_mmo()
            f.write(self.lastkey_mmo)
            f.close()

    def new_mmo(self):
        r = requests.get(self.url)
        html = BS(r.content, 'html.parser')

        new = ''
        items = html.find('div',class_='title').find('a').get('href')

        key = self.parse_href(items)
        if (self.lastkey_mmo != key):
            new = key

        return new

    def mmo_info(self):
        r = requests.get(self.url, headers=self.HEADERS)
        soup = BS(r.content, 'html.parser')
        link = soup.find('div',class_='title').find('a').get('href')


        poster = soup.find('div',class_='image').find('img').get('src').replace('X','T')

        info = {
            "title": soup.find('div',class_='title').find('a').get_text(),
            "link": link,
            "image": poster,
            "text": soup.find('div',class_='shortly').get_text()
        }

        return info

    def download_image_mmo(self, url):
        r = requests.get(url, allow_redirects=True)

        a = urlparse(url)
        filename = os.path.basename(a.path)
        open(filename, 'wb').write(r.content)

        return filename

    def get_lastkey_mmo(self):
        r = requests.get(self.url)
        html = BS(r.content, 'html.parser')

        items = html.find('div',class_='title').find('a').get('href')
        return self.parse_href(items)

    def parse_href(self, href):
        r = requests.get(self.url)
        html = BS(r.content, 'html.parser')

        result= html.find('div',class_='title').find('a').get('href')
        self.newkey = result
        return result

    def update_lastkey_mmo(self):
        self.lastkey_mmo = self.newkey

        with open(self.lastkey_mmo_file, "r+") as f:
            data = f.read()
            f.seek(0)
            f.write(str(self.newkey))
            f.truncate()
        return self.newkey