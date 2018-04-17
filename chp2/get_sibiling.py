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
all_gift_list = bs_obj.find("table", {"id" : "giftList"}).tr.next_siblings

for gift_list in all_gift_list:
    print("-------------------")
    print(gift_list)
