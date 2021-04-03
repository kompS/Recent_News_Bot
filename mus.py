import re
import os.path
import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse

class Music:
	host = 'https://newsmuz.com'
	url = 'https://newsmuz.com/news'
	HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.424','accept': '*/*'}

	newkey = ""
	lastkey_mus = ""
	lastkey_mus_file = ""

	def __init__(self, lastkey_mus_file):
		self.lastkey_mus_file = lastkey_mus_file

		if(os.path.exists(lastkey_mus_file)):
			self.lastkey_mus = open(lastkey_mus_file, 'r').read()
		else:
			f = open(lastkey_mus_file, 'w')
			self.lastkey_mus = self.get_lastkey_mus()
			f.write(self.lastkey_mus)
			f.close()

	def new_mus(self):
		r = requests.get(self.url)
		html = BS(r.content, 'html.parser')

		new = ''
		items = html.find('span',class_='field-content zag').find('a').get('href')

		key = self.parse_href(items)
		if(self.lastkey_mus != key):
			new = key

		return new

	def mus_info(self):
		r = requests.get(self.url,headers=self.HEADERS)
		soup = BS(r.content, 'html.parser')
		link = soup.find('span',class_='field-content zag').find('a').get('href')

		postlink = self.host + link
		rr = requests.get(postlink,headers=self.HEADERS)
		newsoup = BS(rr.content, 'html.parser')

		poster = soup.find('div',class_='field-content').find('img').get('src')

		info = {
			"title": soup.find('span',class_='field-content zag').find('a').get_text(),
			"link": postlink,
			"image": poster,
			"text": newsoup.find('div',class_='field-item even').find_next('div',class_='field-item even').get_text()
		};	
	
		return info

	def download_image_mus(self, url):
		r = requests.get(url, allow_redirects=True)

		a = urlparse(url)
		filename = os.path.basename(a.path)
		open(filename, 'wb').write(r.content)

		return filename

	def get_lastkey_mus(self):
		r = requests.get(self.url)
		html = BS(r.content, 'html.parser')

		items = html.find('span',class_='field-content zag').find('a').get('href')
		return self.parse_href(items)

	def parse_href(self, href):
		result = re.search(r'\d+', href)
		self.newkey = result.group(0)
		return result.group(0)

	def update_lastkey_mus(self):
		self.lastkey_mus = self.newkey

		with open(self.lastkey_mus_file, "r+") as f:
			data = f.read()
			f.seek(0)
			f.write(str(self.newkey))
			f.truncate()
		return self.newkey

