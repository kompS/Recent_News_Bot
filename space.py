import re
import os.path
import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse


class Space:
    url = 'https://www.space.com/news'
    host = 'https://www.space.com/'
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.259','accept': '*/*'}


    newkey = ""
    lastkey_space = ""
    lastkey_space_file = ""

    def __init__(self, lastkey_space_file):
        self.lastkey_space_file = lastkey_space_file

        if (os.path.exists(lastkey_space_file)):
            self.lastkey_space = open(lastkey_space_file, 'r').read()
        else:
            f = open(lastkey_space_file, 'w')
            self.lastkey_space = self.get_lastkey_space()
            f.write(self.lastkey_space)
            f.close()

    def new_space(self):
        r = requests.get(self.url)
        html = BS(r.content, 'html.parser')

        new = ''
        items = html.find('div',class_='listingResult small result1').find('a').get('href')

        key = self.parse_href(items)
        if (self.lastkey_space != key):
            new = key

        return new

    def space_info(self):
        r = requests.get(self.url, headers=self.HEADERS)
        soup = BS(r.content, 'html.parser')
        link = soup.find('div',class_='listingResult small result1').find('a').get('href')

        
        rr = requests.get(link, headers=self.HEADERS)
        newsoup = BS(rr.content, 'html.parser')

        poster = soup.find('div',class_='image-remove-reflow-container landscape').get('data-original')

        info = {
            "title": soup.find('h3',class_='article-name').get_text(),
            "link": link,
            "image": poster,
            "text": soup.find('p',class_='synopsis').get_text()
        }

        return info

    def download_image_space(self, url):
        r = requests.get(url, allow_redirects=True)

        a = urlparse(url)
        filename = os.path.basename(a.path)
        open(filename, 'wb').write(r.content)

        return filename

    def get_lastkey_space(self):
        r = requests.get(self.url)
        html = BS(r.content, 'html.parser')

        items = html.find('div',class_='listingResult small result1').find('a').get('href')
        return self.parse_href(items)

    def parse_href(self, href):
        r = requests.get(self.url)
        html = BS(r.content, 'html.parser')

        result= html.find('div',class_='listingResult small result1').find('a').get('href')
        self.newkey = result
        return result

    def update_lastkey_space(self):
        self.lastkey_space = self.newkey

        with open(self.lastkey_space_file, "r+") as f:
            data = f.read()
            f.seek(0)
            f.write(str(self.newkey))
            f.truncate()
        return self.newkey