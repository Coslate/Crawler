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
all_child = bs_obj.find("table", {"id" : "giftList"}).children
all_child = [x for x in all_child if x is not None]

for child in all_child:
    print("-------------------")
    print(child)
