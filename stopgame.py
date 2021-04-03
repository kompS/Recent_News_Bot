import re
import os.path
import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse

class StopGame:
	host = 'https://stopgame.ru'
	url = 'https://stopgame.ru/news'
	HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.323','accept': '*/*'}
	newkey = ""
	lastkey = ""
	lastkey_file = ""

	def __init__(self, lastkey_file):
		self.lastkey_file = lastkey_file

		if(os.path.exists(lastkey_file)):
			self.lastkey = open(lastkey_file, 'r').read()
		else:
			f = open(lastkey_file, 'w')
			self.lastkey = self.get_lastkey()
			f.write(self.lastkey)
			f.close()

	def new_games(self):
		r = requests.get(self.url)
		html = BS(r.content, 'html.parser')

		new = ''
		items = html.find('div',class_='caption caption-bold').find('a').get('href')
		key = self.parse_href(items)
		if(self.lastkey < key):
			new = key

		return new

	def game_info(self):
		r = requests.get(self.url)
		soup = BS(r.content, 'html.parser')
		link = soup.find('div',class_='caption caption-bold').find('a').get('href')
		postlink = self.host + link


		newr = requests.get(postlink,headers=self.HEADERS)
		newsoup = BS(newr.content, 'html.parser')

		
		poster = soup.find('img', class_='image-16x9').get('src')

		info = {
			"title": newsoup.find('h1',class_='article-title').get_text(),
			"link": postlink,
			"image": poster,
			"text": newsoup.find('section',class_='article').find('p').get_text()
		};	
	
		return info

	def download_image(self, url):
		r = requests.get(url, allow_redirects=True)

		a = urlparse(url)
		filename = os.path.basename(a.path)
		open(filename, 'wb').write(r.content)

		return filename


	def get_lastkey(self):
		r = requests.get(self.url)
		html = BS(r.content, 'html.parser')

		items = html.find('div',class_='caption caption-bold').find('a').get('href')
		return self.parse_href(items['href'])

	def parse_href(self, href):
		result = re.search(r'\d+', href)
		self.newkey = result.group(0)
		return result.group(0)

	def update_lastkey(self):
		self.lastkey = self.newkey

		with open(self.lastkey_file, "r+") as f:
			data = f.read()
			f.seek(0)
			f.write(str(self.newkey))
			f.truncate()
		return self.newkey
