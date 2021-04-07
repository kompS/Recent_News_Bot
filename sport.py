import re
import os.path
import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse


class Sport:
    host = 'https://life.ru'
    url = 'https://life.ru/c/sport'
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.424',
        'accept': '*/*'
    }

    newkey = ""
    lastkey_sport = ""
    lastkey_sport_file = ""

    def __init__(self, lastkey_sport_file):
        self.lastkey_sport_file = lastkey_sport_file

        if (os.path.exists(lastkey_sport_file)):
            self.lastkey_sport = open(lastkey_sport_file, 'r').read()
        else:
            f = open(lastkey_sport_file, 'w')
            self.lastkey_sport = self.get_lastkey_sport()
            f.write(self.lastkey_sport)
            f.close()

    def new_sport(self):
        r = requests.get(self.url)
        html = BS(r.content, 'html.parser')

        new = ''
        items = html.find('div', class_='row').find('a').get('href')

        key = self.parse_href(items)
        if (self.lastkey_sport != key):
            new = key

        return new

    def sport_info(self):
        r = requests.get(self.url, headers=self.HEADERS)
        soup = BS(r.content, 'html.parser')
        link = soup.find('div', class_='row').find('a').get('href')

        postlink = self.host + link

        rr = requests.get(postlink, headers=self.HEADERS)
        newsoup = BS(rr.content, 'html.parser')

        poster = soup.find('div', class_='styles_pic__2Hno5 styles_loaded__3jlQD').find('img').get('src')

        info = {
            "title": newsoup.find('h1', class_='styles_title__2F4Y1').get_text(),
            "link": postlink,
            "image": poster,
            "text": newsoup.find('div', class_='marginRules_block__1eVKw styles_text__fxCxY').find('p').get_text()
        }

        return info

    def download_image_sport(self, url):
        r = requests.get(url, allow_redirects=True)

        a = urlparse(url)
        filename = os.path.basename(a.path)
        open(filename, 'wb').write(r.content)

        return filename

    def get_lastkey_sport(self):
        r = requests.get(self.url)
        html = BS(r.content, 'html.parser')

        items = html.find('div', class_='row').find('a').get('href')
        return self.parse_href(items)

    def parse_href(self, href):
        result = re.search(r'\d+', href)
        self.newkey = result.group(0)
        return result.group(0)

    def update_lastkey_sport(self):
        self.lastkey_sport = self.newkey

        with open(self.lastkey_sport_file, "r+") as f:
            data = f.read()
            f.seek(0)
            f.write(str(self.newkey))
            f.truncate()
        return self.newkey
