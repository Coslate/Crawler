#! /usr/bin/env python3.6
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

def GetTitle(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
        return None
    try:
        bs4_obj = BeautifulSoup(html.read(), "html.parser")
        title = bs4_obj.body.h1
    except AttributeError as e:
        print(e)
        return None
    return title

def main():
    title = GetTitle("http://pythonscraping.com/pages/page1.html")
    if(title is None):
        print("Title is not found.")
    else:
        print("Title = {}".format(title.get_text()))

#---------------Execution---------------#
if __name__ == '__main__':
    main()
