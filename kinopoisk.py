import re
import os.path
import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse

class Kinopoisk:
	host = 'https://www.kinopoisk.ru'
	url = 'https://www.kinopoisk.ru/media/news'
	HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0', 'accept': '*/*'}
	newkey = ""
	lastkey_kino = ""
	lastkey_kino_file = ""

	def __init__(self, lastkey_kino_file):
		self.lastkey_kino_file = lastkey_kino_file

		if(os.path.exists(lastkey_kino_file)):
			self.lastkey_kino = open(lastkey_kino_file, 'r').read()
		else:
			f = open(lastkey_kino_file, 'w')
			self.lastkey_kino = self.get_lastkey_kino()
			f.write(self.lastkey_kino)
			f.close()

	def new_kino(self):
		r = requests.get(self.url)
		html = BS(r.content, 'html.parser')

		new = ''
		items = html.find('a', class_='post-feature-card__link').get('href')

		key = self.parse_href(items)
		if(self.lastkey_kino != key):
			new = key

		return new

	def kino_info(self):
		r = requests.get(self.url,headers=self.HEADERS)
		soup = BS(r.content, 'html.parser')
		link = soup.find('a', class_='post-feature-card__link').get('href')
#http://avatars.mds.yandex.net/get-kinopoisk-post-thumb/1540726/07e5adbfd5d86830c8ead43fce6267a7/640x360
		postlink = self.host + link

		rr = requests.get(postlink,headers=self.HEADERS)
		newsoup = BS(rr.content, 'html.parser')

		poster = 'http:' + soup.find('div', class_='post-feature-card__main-image-wrapper').find('img').get('src')
		info = {
			"title": newsoup.find('h1', class_='media-post-title').find('span').get_text(),
			"link": postlink,
			"image": poster,
			"text": newsoup.find('div', class_='stk-post').find('p').get_text()
		};	
	
		return info

	def download_image_kino(self, url):
		r = requests.get(url, allow_redirects=True)

		a = urlparse(url)
		filename = os.path.basename(a.path)
		open(filename, 'wb').write(r.content)

		return filename

	def get_lastkey_kino(self):
		r = requests.get(self.url)
		html = BS(r.content, 'html.parser')

		items = html.find('a', class_='post-feature-card__link').get('href')
		return self.parse_href(items)

	def parse_href(self, href):
		result = re.search(r'\d+', href)
		self.newkey = result.group(0)
		return result.group(0)

	def update_lastkey_kino(self):
		self.lastkey_kino = self.newkey

		with open(self.lastkey_kino_file, "r+") as f:
			data = f.read()
			f.seek(0)
			f.write(str(self.newkey))
			f.truncate()
		return self.newkey

