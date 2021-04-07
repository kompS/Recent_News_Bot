import re
import os.path
import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse


class Anime:
    host = 'https://kg-portal.ru'
    url = 'https://kg-portal.ru/news/anime/'
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.424',
        'accept': '*/*'
        }
    newkey = ""
    lastkey_anim = ""
    lastkey_anim_file = ""

    def __init__(self, lastkey_anim_file):
        self.lastkey_anim_file = lastkey_anim_file

        if (os.path.exists(lastkey_anim_file)):
            self.lastkey_anim = open(lastkey_anim_file, 'r').read()
        else:
            f = open(lastkey_anim_file, 'w')
            self.lastkey_anim = self.get_lastkey_anime()
            f.write(self.lastkey_anim)
            f.close()

    def new_anime(self):
        r = requests.get(self.url)
        html = BS(r.content, 'html.parser')

        new = ''
        items = html.find('div', class_="news_sources").find_next('a').find_next('a').find_next('a').get('href')

        key = self.parse_href(items)
        if (self.lastkey_anim != key):
            new = key

        return new

    def anime_info(self):
        r = requests.get(self.url, headers=self.HEADERS)
        soup = BS(r.content, 'html.parser')
        link = soup.find('div', class_="news_box anime_cat").find_next('a').find_next('a').find_next('a').get('href')

        postlink = self.host + link

        rr = requests.get(postlink, headers=self.HEADERS)
        newsoup = BS(rr.content, 'html.parser')

        # try:
        poster = self.host + newsoup.find('div', class_='news_cover_center').find('img').get('src')
        # except:
        #     poster = newsoup.find('img', class_='splash').get('src')

        info = {
            "title": newsoup.find('h1', class_="news_title").get_text(),
            "link": postlink,
            "image": poster,
            "text": newsoup.find('div', class_="news_text").find('p').get_text()
        }

        return info

    def download_image_anime(self, url):
        r = requests.get(url, allow_redirects=True)

        a = urlparse(url)
        filename = os.path.basename(a.path)
        open(filename, 'wb').write(r.content)

        return filename

    def get_lastkey_anime(self):
        r = requests.get(self.url)
        html = BS(r.content, 'html.parser')

        items = html.find('div', class_="news_sources").find_next('a').find_next('a').find_next('a').get('href')
        return self.parse_href(items)

    def parse_href(self, href):
        result = re.search(r'\d+', href)
        self.newkey = result.group(0)
        return result.group(0)

    def update_lastkey_anime(self):
        self.lastkey_anim = self.newkey

        with open(self.lastkey_anim_file, "r+") as f:
            data = f.read()
            f.seek(0)
            f.write(str(self.newkey))
            f.truncate()
        return self.newkey
