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
price = bs_obj.find("img", {"src" : "../img/gifts/img1.jpg"}).parent.previous_sibling.get_text()
print(f"price = {price}")

