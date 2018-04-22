#! /usr/bin/env python3.6

import requests
from   urllib.request import urlopen
from   urllib.error import HTTPError
from   bs4 import BeautifulSoup
import re

def main():
    #--------------------------------------------------------------
    #Step1. Use "Get" Request to Get PTT Web Response
    #--------------------------------------------------------------
    url = "https://www.ptt.cc/bbs/nba/index.html"

    try:
        #html = urlopen(url) # will error due to forbidding crawler of ptt.
        response = requests.get(url)
    except HTTPError as e :
        print(e)

    print(f"type(response) = {type(response)}")

    #--------------------------------------------------------------
    #Step2. Use "Beautifulsoup" to Find the Wanted Title
    #--------------------------------------------------------------
    soup = BeautifulSoup(response.text, 'lxml')
    articles = soup.find_all('div', {"class":"r-ent"})

    for article in articles:
        print("=========")
        title    = GetStrValue(article.find('div', 'title').find('a'), 0)
        push_num = GetStrValue(article.find('div', 'nrec').find('span', {"class":re.compile("^hl\s*.*")}), 1)
        date     = GetStrValue(article.find('div', 'meta').find('div', {"class":"date"}), 0)
        author   = GetStrValue(article.find('div', 'meta').find('div', {"class":"author"}), 0)

        print(f"type(article) = {type(article)}")
        print(f"title    = {title}")
        print(f"push_num = {push_num}")
        print(f"date     = {date}")
        print(f"author   = {author}")
    #    print(f"article       = {article}")




def GetStrValue(tag, numeric_if_none):
    if(tag == None):
        if(numeric_if_none):
            return 0
        else:
            return "None"
    else:
        return tag.get_text().strip()


#---------------Execution---------------#
if __name__ == '__main__':
    main()
