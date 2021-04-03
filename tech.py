import re
import os.path
import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse

class Tech:
	host = 'https://gagadget.com'
	url = 'https://gagadget.com/news/'
	HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.424','accept': '*/*'}

	newkey = ""
	lastkey_tech = ""
	lastkey_tech_file = ""

	def __init__(self, lastkey_tech_file):
		self.lastkey_tech_file = lastkey_tech_file

		if(os.path.exists(lastkey_tech_file)):
			self.lastkey_tech = open(lastkey_tech_file, 'r').read()
		else:
			f = open(lastkey_tech_file, 'w')
			self.lastkey_tech= self.get_lastkey_tech()
			f.write(self.lastkey_tech)
			f.close()

	def new_tech(self):
		r = requests.get(self.url)
		html = BS(r.content, 'html.parser')

		new = ''
		items = html.find('span',class_='cell-title').find('a').get('href')

		key = self.parse_href(items)
		if(self.lastkey_tech < key):
			new = key

		return new

	def tech_info(self):
		r = requests.get(self.url,headers=self.HEADERS)
		soup = BS(r.content, 'html.parser')
		link = soup.find('span',class_='cell-title').find('a').get('href')

		postlink = self.host + link

		rr = requests.get(postlink,headers=self.HEADERS)
		newsoup = BS(rr.content, 'html.parser')

		poster = self.host + newsoup.find('img',class_='js-album').get('src')

		info = {
			"title": newsoup.find('div',class_='b-nodetop b-nodetop_nobor').find('h1').get_text(),
			"link": postlink,
			"image": poster,
			"text": newsoup.find('div',class_='b-font-def post-links').find('p').find_next('p').get_text()
		};	
	
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

		items = html.find('span',class_='cell-title').find('a').get('href')
		return self.parse_href(items)

	def parse_href(self, href):
		result = re.search(r'\d+', href)
		self.newkey = result.group(0)
		return result.group(0)

	def update_lastkey_tech(self):
		self.lastkey_tech = self.newkey

		with open(self.lastkey_tech_file, "r+") as f:
			data = f.read()
			f.seek(0)
			f.write(str(self.newkey))
			f.truncate()
		return self.newkey
