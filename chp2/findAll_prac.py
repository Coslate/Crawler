#! /usr/bin/env python3.6

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup


def main():
    url = "http://www.pythonscraping.com/pages/warandpeace.html"
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)

    bs_obj = BeautifulSoup(html, "html.parser")
    #attr is the "or" fiter. keyword is the "and" filter
    #find the "span" tag with (class = green | red) & (class = green)
    name_list = bs_obj.findAll("span", {"class":{"green", "red"}}, class_ = "green")
    #name_list = bs_obj.findAll(["h2", "h1"])
    prince_list = bs_obj.findAll(text = "The prince")

    print(f"len(prince_list) = {len(prince_list)}")
    for ele in prince_list:
        print(f"type(ele) = {type(ele)}")
        print(f"ele = {ele}")

    for name in name_list:
        print("---")
        print(f"type(name) = {type(name)}")
        print(f"name = {name}")
        print(f"name.get_text() = {name.get_text()}")

#---------------Execution---------------#
if __name__ == '__main__':
    main()

