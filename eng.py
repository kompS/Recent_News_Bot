import re
import os.path
import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse

class Eng:
	host = 'https://www.theverge.com'
	url = 'https://www.theverge.com/games'
	HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.424','accept': '*/*'}
	newkey = ""
	lastkey_eng = ""
	lastkey_eng_file = ""

	def __init__(self, lastkey_eng_file):
		self.lastkey_eng_file = lastkey_eng_file

		if(os.path.exists(lastkey_eng_file)):
			self.lastkey_eng = open(lastkey_eng_file, 'r').read()
		else:
			f = open(lastkey_eng_file, 'w')
			self.lastkey_eng = self.get_lastkey_eng()
			f.write(self.lastkey_eng)
			f.close()

	def new_daily(self):
		r = requests.get(self.url)
		html = BS(r.content, 'html.parser')

		new = ''
		items = html.find('h2',class_='c-entry-box--compact__title').find('a').get('href')

		key = self.parse_href(items)
		if(self.lastkey_eng < key):
			new = key

		return new

	def daily_info(self):
		r = requests.get(self.url,headers=self.HEADERS)
		soup = BS(r.content, 'html.parser')
		link = soup.find('h2',class_='c-entry-box--compact__title').find('a').get('href')


		rr = requests.get(link,headers=self.HEADERS)
		newsoup = BS(rr.content, 'html.parser')

		poster = newsoup.find('picture', class_='c-picture').find('img').get('src')

		info = {
			"title": newsoup.find('h1',class_='c-page-title').get_text(),
			"link": link,
			"image": poster,
			"text": newsoup.find('div',class_='c-entry-content').find('p').get_text()
		};	
	
		return info



	def download_image_eng(self, url):
		r = requests.get(url, allow_redirects=True)

		a = urlparse(url)
		filename = os.path.basename(a.path)
		open(filename, 'wb').write(r.content)

		return filename

	def get_lastkey_eng(self):
		r = requests.get(self.url)
		html = BS(r.content, 'html.parser')

		items = html.find('h2',class_='c-entry-box--compact__title').find('a').get('href')
		return self.parse_href(items)

	def parse_href(self, href):
		result = re.search(r'\d{8}', href)
		self.newkey = result.group(0)
		return result.group(0)

	def update_lastkey_eng(self):
		self.lastkey_eng = self.newkey

		with open(self.lastkey_eng_file, "r+") as f:
			data = f.read()
			f.seek(0)
			f.write(str(self.newkey))
			f.truncate()
		return self.newkey

