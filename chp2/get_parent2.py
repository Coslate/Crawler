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
img = bs_obj.find(text=re.compile("\$15")).parent.next_sibling.img
print(f"image = {img['src']}")

