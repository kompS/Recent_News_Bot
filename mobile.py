import re
import os.path
import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse


class Mobile:
    url = 'https://gurugamer.com/mobile-games'
    host = 'https://gurugamer.com'
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.259','accept': '*/*'}

    newkey = ""
    lastkey_mob = ""
    lastkey_mob_file = ""

    def __init__(self, lastkey_mob_file):
        self.lastkey_mob_file = lastkey_mob_file

        if (os.path.exists(lastkey_mob_file)):
            self.lastkey_mob = open(lastkey_mob_file, 'r').read()
        else:
            f = open(lastkey_mob_file, 'w')
            self.lastkey_mob = self.get_lastkey_mob()
            f.write(self.lastkey_mob)
            f.close()

    def new_mob(self):
        r = requests.get(self.url)
        html = BS(r.content, 'html.parser')

        new = ''
        items = html.find('figure',class_='news-hot-big news-hot-big-cate').find('a').get('href')

        key = self.parse_href(items)
        if (self.lastkey_mob != key):
            new = key

        return new

    def mob_info(self):
        r = requests.get(self.url, headers=self.HEADERS)
        soup = BS(r.content, 'html.parser')
        link = soup.find('figure',class_='news-hot-big news-hot-big-cate').find('a').get('href')

        postlink = self.host + link

        rr = requests.get(postlink, headers=self.HEADERS)
        newsoup = BS(rr.content, 'html.parser')

        
        poster = soup.find('a',class_='image').find('img').get('data-src')
        
        info = {
            "title": soup.find('h2',class_='h').get_text(),
            "link": postlink,
            "image": poster,
            "text": newsoup.find('div', class_='desciption post-content content-news').find('p').get_text()
        }

        return info

    def download_image_mob(self, url):
        r = requests.get(url, allow_redirects=True)

        a = urlparse(url)
        filename = os.path.basename(a.path)
        open(filename, 'wb').write(r.content)

        return filename

    def get_lastkey_mob(self):
        r = requests.get(self.url)
        html = BS(r.content, 'html.parser')

        items = html.find('figure',class_='news-hot-big news-hot-big-cate').find('a').get('href')
        return self.parse_href(items)

    def parse_href(self, href):
        r = requests.get(self.url)
        html = BS(r.content, 'html.parser')

        result= html.find('figure',class_='news-hot-big news-hot-big-cate').find('a').get('href')
        self.newkey = result
        return result

    def update_lastkey_mob(self):
        self.lastkey_mob = self.newkey

        with open(self.lastkey_mob_file, "r+") as f:
            data = f.read()
            f.seek(0)
            f.write(str(self.newkey))
            f.truncate()
        return self.newkey