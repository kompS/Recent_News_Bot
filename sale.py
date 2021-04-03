import re
import os.path
import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse

class Sale:
	host = 'https://www.igromania.ru'
	url = 'https://www.igromania.ru/news/sale/'
	HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.424','accept': '*/*'}

	newkey = ""
	lastkey_sale = ""
	lastkey_sale_file = ""

	def __init__(self, lastkey_sale_file):
		self.lastkey_sale_file = lastkey_sale_file

		if(os.path.exists(lastkey_sale_file)):
			self.lastkey_sale = open(lastkey_sale_file, 'r').read()
		else:
			f = open(lastkey_sale_file, 'w')
			self.lastkey_sale= self.get_lastkey_sale()
			f.write(self.lastkey_sale)
			f.close()

	def new_sale(self):
		r = requests.get(self.url)
		html = BS(r.content, 'html.parser')

		new = ''
		items = html.find('div',class_='aubli_data').find('a').get('href')

		key = self.parse_href(items)
		if(self.lastkey_sale != key):
			new = key

		return new

	def sale_info(self):
		r = requests.get(self.url,headers=self.HEADERS)
		soup = BS(r.content, 'html.parser')
		link = soup.find('div',class_='aubli_data').find('a').get('href')

		postlink = self.host + link

		rr = requests.get(postlink,headers=self.HEADERS)
		newsoup = BS(rr.content, 'html.parser')

		poster = newsoup.find('div',class_='main_pic_container').find('img').get('src')

		info = {
			"title": soup.find('div',class_='aubli_data').find('a').get_text(),
			"link": postlink,
			"image": poster,
			"text": newsoup.find('div',class_='universal_content clearfix').find('div').get_text() + "\n\n" + newsoup.find('div',class_='universal_content clearfix').find('div').find_next('div').get_text()
		};	
	
		return info

	def download_image_sale(self, url):
		r = requests.get(url, allow_redirects=True)

		a = urlparse(url)
		filename = os.path.basename(a.path)
		open(filename, 'wb').write(r.content)

		return filename

	def get_lastkey_sale(self):
		r = requests.get(self.url)
		html = BS(r.content, 'html.parser')

		items = html.find('div',class_='aubli_data').find('a').get('href')
		return self.parse_href(items)

	def parse_href(self, href):
		result = re.search(r'\d+', href)
		self.newkey = result.group(0)
		return result.group(0)

	def update_lastkey_sale(self):
		self.lastkey_sale = self.newkey

		with open(self.lastkey_sale_file, "r+") as f:
			data = f.read()
			f.seek(0)
			f.write(str(self.newkey))
			f.truncate()
		return self.newkey
