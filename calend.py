import re
import os.path
import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse

class Calend:
	url = 'https://www.calend.ru/events/'
	HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.424','accept': '*/*'}

	def calend_info(self):
		r = requests.get(self.url)
		soup = BS(r.content, 'html.parser')
		
		poster = soup.find_all('div', class_='image')

		info = {
			"title": soup.find_all('div',class_='caption'),
			"image": poster,
			"year": soup.find_all('span',class_='year')
		};	
	
		return info

	def download_image_cal(self, url):
		r = requests.get(url, allow_redirects=True)

		a = urlparse(url)
		filename = os.path.basename(a.path)
		open(filename, 'wb').write(r.content)

		return filename	

