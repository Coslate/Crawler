#! /usr/bin/env python3.6

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

try:
    html = urlopen("https://en.wikipedia.org/wiki/Kevin_Bacon")
except HTTPError as e:
    print(e)

bs_obj = BeautifulSoup(html, "html.parser")
for link in bs_obj.findAll("a"):
    print(f"link = {link}")
    print(f"link.attrs = {link.attrs}")
    if('href' in link.attrs):
        print(link['href'])
    print("--------------")

