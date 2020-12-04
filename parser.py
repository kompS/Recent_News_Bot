import re
import os.path
import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse


host = 'https://stopgame.ru'
url = 'https://stopgame.ru/news'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.323','accept': '*/*'}
lastkey = ""
newkey = "45859"
lastkey_file = "lastkey.txt"

def init(lastkey_file):
	lastkey_file = lastkey_file

	if(os.path.exists(lastkey_file)):
		lastkey = open(lastkey_file, 'r').read()
	else:
		f = open(lastkey_file, 'w')
		lastkey = get_lastkey()
		f.write(lastkey)
		f.close()

def new_games():
	r = requests.get(url)
	html = BS(r.content, 'html.parser')

	new = ''
	items = html.find('div',class_='caption caption-bold').find('a').get('href')
	key = parse_href(items)
	if(lastkey < key):
		new = key

	return new

def get_content(url):
	r = requests.get(url,headers=HEADERS)
	soup = BS(r.content, 'html.parser')
	link = soup.find('div',class_='caption caption-bold').find('a').get('href')
	postlink = host + link

	newr = requests.get(postlink,headers=HEADERS)
	newsoup = BS(newr.content, 'html.parser')
	title = newsoup.find('h1',class_='article-title').get_text()
	text1 = newsoup.find('section',class_='article').find('p').get_text()
	info = {
			"title": newsoup.find('h1',class_='article-title').get_text(),
			"link": postlink,
			"text": newsoup.find('section',class_='article').find('p').get_text()
		};	
	items = soup.find('div',class_='caption caption-bold').find('a').get('href')
	print(items)
	return info

def get_lastkey():
		r = requests.get(url)
		html = BS(r.content, 'html.parser')

		items = html.find('div',class_='caption caption-bold').find('a').get('href')
		return parse_href(items)

def parse_href(href):
	result = re.search(r'\d+', href)
	newkey = result.group(0)
	return result.group(0)

def update_lastkey(new_key):
	lastkey = new_key

	with open(lastkey_file, "r+") as f:
		data = f.read()
		f.seek(0)
		f.write(str(new_key))
		f.truncate()
	return new_key

update_lastkey(newkey)
