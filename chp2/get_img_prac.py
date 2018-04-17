#! /usr/bin/env python3.6

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re

try:
    html = urlopen("http://www.pythonscraping.com/pages/page3.html")
except HTTPError as e :
    print(e)

bs_obj = BeautifulSoup(html, "html.parser")
images = bs_obj.findAll("img", {"src":re.compile("\.\.\/img\/gifts\/.*\.jpg")})

for image in images:
    print("================")
    print("image[\'src\'] = ", image['src'])
    print("image.get(\'src\') = ", image.get('src'))
    print("image.img = ", image.img)
    print("image = ", image)
    print("type(image) = ", type(image))
