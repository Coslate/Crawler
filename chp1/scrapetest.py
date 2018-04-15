#! /usr/bin/env python3.6
from urllib.request import urlopen as Uop
from bs4 import BeautifulSoup as BS4Soup

html = Uop("http://pythonscraping.com/pages/page1.html")
bs_obj = BS4Soup(html.read(), "html.parser")

print("bs_obj.html.body.h1 = ", bs_obj.html.body.h1)
print("bs_obj.html.h1 = ", bs_obj.html.h1)
print("bs_obj.body.h1 = ", bs_obj.body.h1)
print("bs_obj.h1 = ", bs_obj.h1)
#print(bs_obj)
#print(html.read())


#bs_obj_local_html = BS4Soup("./simple_prac.html", "html.parser")
#print("bs_obj_local_html.h2 = ", bs_obj_local_html.h2)
