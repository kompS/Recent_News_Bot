import re
import os.path
import requests

from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse

from google_trans_new import google_translator

transl = google_translator()
host = 'https://newsmuz.com'
url = 'https://newsmuz.com/news'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.424','accept': '*/*'}

r = requests.get(url,HEADERS)
soup = BS(r.content, 'html.parser')

#url1 = 'https://kg-portal.ru/comments/95407-klub-detektivovkrasavchikov-videoprevju-endinga-v-ispolnenii-detektivovkrasavchikov/'

#poster = soup.find('div', class_='image').find('a').find('img').get('src')

#link = soup.find('div',class_='science_heroes').find('a').get('href')



link = soup.find('span',class_='field-content zag').find('a').get('href')
postlink = host + link

title = soup.find('span',class_='field-content zag').find('a').get_text()

newr = requests.get(postlink,HEADERS)
newsoup = BS(newr.content, 'html.parser')

text = newsoup.find('div',class_='field-items').next_element().next_element().find('p').get_text()

image = soup.find('div',class_='field-content').find('img').get('src')



print(text)