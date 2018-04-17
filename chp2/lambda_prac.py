#! /usr/bin/env python3.6

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

try:
    html = urlopen("http://www.pythonscraping.com/pages/page3.html")
except HTTPError as e:
    print(e)
bs_obj = BeautifulSoup(html.read(), "html.parser")
find_obj = bs_obj.findAll(lambda tag: len(tag.attrs) == 2)

print(type(find_obj))
print("")

for element in find_obj:
    print(f"type(element) = {type(element)}")
    print(f"element = {element}")
