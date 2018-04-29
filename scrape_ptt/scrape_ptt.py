#! /usr/bin/env python3.6
'''
    Author      : Coslate
    Date        : 2018/04/25
    Description :
        This program will scrape the PTT NBA forum and copy the content to
        your local with the naming rule, "{title}_{date}_{author}_{push_num}.txt".
        One can input the parameter -et {date} to get all the articles after {date}
        One can input the parameter -st {date} to get all the articles before {date}
        One can input the parameter -key {word} to get all the articles that include the keyword : {word}
        One can input the parameter -out {output_directory} to write out the articles to {output_directory}
        One can input the parameter -isd {1/0} to get print out the debug messages
'''

import urllib.parse as urlparse
import requests
from   urllib.request import urlopen
from   urllib.error import HTTPError
from   bs4 import BeautifulSoup
import re
import argparse
import datetime
import sys

#########################
#     Main-Routine      #
#########################
def main():
    #Initial URL
    url = "https://www.ptt.cc/bbs/nba/index.html"
    month_dic = {"Jan":"01",
                 "Feb":"02",
                 "Mar":"03",
                 "Apr":"04",
                 "May":"05",
                 "Jun":"06",
                 "Jul":"07",
                 "Aug":"08",
                 "Sep":"09",
                 "Oct":"10",
                 "Nov":"11",
                 "Dec":"12"}

    #Process the argument
    start_time      = datetime.datetime.now()
    start_time      = re.match(r"(\d+)\-(\d+)\-(\d+)\s.*", str(start_time)).groups()
    start_time      = int(start_time[0]+start_time[1]+start_time[2])
    end_time        = None
    (start_time, end_time, keyword, out_dir, is_debug) = ArgumentParser(start_time)

    #Scraping all the related articles
    articles_dic_arr = GetAllThePages(start_time, end_time, keyword, url, month_dic, is_debug);

    for articles_dic in articles_dic_arr:
        title = articles_dic['title']
        pattern = re.compile(r'\s*')
        title = re.sub(pattern, '', title)
        title = title.replace('[', '_')
        title = title.replace(']', '_')
        file_name = title+"_"+articles_dic['date_reform']+"_"+articles_dic['author']+'_'+articles_dic['push_num']+".txt"
        with open('{x}/{y}'.format(x = out_dir, y = file_name), 'w') as out_file:
            out_file.write(articles_dic['content_info'])
        out_file.closed

    #Print the debug messages when necessary
    if(is_debug):
        print(f"start_time = {start_time}")
        print(f"end_time = {end_time}")
        print(f"keyword = {keyword}")

        for articles_dic in articles_dic_arr:
            print("==========================================")
            print(f"title            = {articles_dic['title']}")
            print(f"date             = {articles_dic['date']}")
            print(f"date_reform      = {articles_dic['date_reform']}")
            print(f"author           = {articles_dic['author']}")
            print(f"push_num         = {articles_dic['push_num']}")
            print(f"link             = {articles_dic['link']}")
            print(f"content          = {articles_dic['content_info']}")


#########################
#     Sub-Routine       #
#########################
def ArgumentParser(start_time):
    end_time        = None
    keyword         = None
    is_debug        = 0

    parser = argparse.ArgumentParser()
    parser.add_argument("--start_time", "-st", help="set the start time of searching articles")
    parser.add_argument("--end_time", "-et", help="set the end time of searching articles")
    parser.add_argument("--keyword", "-key", help="set the keyword that the content of an article will include and be searched")
    parser.add_argument("--out_dir", "-out", help="set the output directory to write out the articles")
    parser.add_argument("--is_debug", "-isd", help="set 1 to check the debug messages")

    args = parser.parse_args()

    if args.start_time:
        start_time = int(args.start_time)
    if args.end_time:
        end_time = int(args.end_time)
    if args.keyword:
        keyword = args.keyword
    if args.out_dir:
        out_dir = args.out_dir
    if args.is_debug:
        is_debug = bool(args.is_debug)

    return (start_time, end_time, keyword, out_dir, is_debug)

def GetStrValue(tag, numeric_if_none):
    if(tag == None):
        if(numeric_if_none):
            return 0
        else:
            return "None"
    else:
        return tag.get_text().strip()

def GetThePageAndUpdateURL(url, articles_dic_arr, start_time, end_time, month_dic, keyword, is_debug):
    #--------------------------------------------------------------
    #Step1. Issue Request.
    #--------------------------------------------------------------
    try:
        response = requests.get(url)
    except HTTPError as e:
        print(e)

    #--------------------------------------------------------------
    #Step2. Interpret Response with Beautifulsoup.
    #--------------------------------------------------------------
    soup         = BeautifulSoup(response.text, 'lxml')
    articles     = soup.find_all('div', {"class":"r-ent"})
    earlest_time = 99999999

    for article in articles:
        title_class = article.find('div', 'title').find('a') or BeautifulSoup('<a>本文已被刪除</a>', 'lxml').a
        title    = GetStrValue(title_class, 0)
        link     = title_class.get('href')
        push_num = GetStrValue(article.find('div', 'nrec').find('span', {"class":re.compile("^hl\s*.*")}), 1)
        date     = GetStrValue(article.find('div', 'meta').find('div', {"class":"date"}), 0)
        author   = GetStrValue(article.find('div', 'meta').find('div', {"class":"author"}), 0)

        if(title == "None"):
            continue

        #Get the link_url to the content
        link_url    = urlparse.urljoin(url, link)

        #Get the detailed timing info of the content
        date_reform = GetTimeInfo(link_url, month_dic, start_time)
        if(date_reform == None):
            continue
        if(int(date_reform) < earlest_time):
            earlest_time = int(date_reform)

        if((int(date_reform) <= int(start_time)) and (int(date_reform) >= int(end_time))):
            #Get the content
            content_info   = GetContentInfo(link_url)
            if(content_info == None):
                continue

            str_line_arr   = content_info.split('\n')
            title_line_arr = title.split('\n')
            l_cnt       = [1 if(len(re.findall(r'{x}'.format(x = keyword), line))) else 0 for line in str_line_arr]
            l_cnt_title = [1 if(len(re.findall(r'{x}'.format(x = keyword), line))) else 0 for line in title_line_arr]

            if((sum(l_cnt) > 0) or (sum(l_cnt_title) > 0)):
                #Store all the information
                articles_dic_arr.append({"title":title, "link":link_url, "push_num":push_num, "date":date, "author":author, "date_reform":date_reform, "content_info":content_info})
            if(is_debug):
                print(f"l_cnt = {l_cnt}")

    #--------------------------------------------------------------
    #Step3. Find the URL of Previous Pages.
    #--------------------------------------------------------------
    link_url = soup.find("div", {"class":re.compile("^btn\-group\s*btn\-group\-paging$")}).find("a", {"class":"btn wide"}, text=re.compile("上頁"))["href"]
    link_url = urlparse.urljoin(url, link_url)

    return (link_url, earlest_time)

def GetAllThePages(start_time, end_time, keyword, url, month_dic, is_debug):
    articles_dic_arr = []
    count_once = 0
    while(True):
        this_loop_article = []
        (url, earlest_time) = GetThePageAndUpdateURL(url, this_loop_article, start_time, end_time, month_dic, keyword, is_debug)
        for each_article in this_loop_article:
            articles_dic_arr.append((each_article))
        if(count_once < 2):
            count_once += 1
        if((int(earlest_time) < int(end_time)) and (count_once > 1)):
            break

    return (articles_dic_arr)

def GetTimeInfo(link_url, month_dic, start_time):
    try:
        response = requests.get(link_url)
    except HTTPError as e:
        print(e)
        sys.exit()

    soup = BeautifulSoup(response.text, 'lxml')

    try:
        time_blk = soup.find('span', 'article-meta-value', text=re.compile("^\S+\s*(\S+)\s*(\S+)\s*\S+\:\S+\:\S+\s*(\S+)\s*")).get_text()
    except AttributeError as e:
        print(e)
        return str(start_time)

    time_match = re.match(r"^\S+\s*(\S+)\s*(\S+)\s*\S+\:\S+\:\S+\s*(\S+)\s*", time_blk)
    month = month_dic[time_match.group(1)]
    year  = time_match.group(3)
    day   = "{:02d}".format(int(time_match.group(2)))

    return(year+month+day)

def GetContentInfo(link_url):
    try:
        response = requests.get(link_url)
    except HTTPError as e:
        print(e)
        print('Respones None')
        sys.exit()

    soup = BeautifulSoup(response.text, 'lxml')
    content_blk = soup.find('div', class_="bbs-screen bbs-content", id='main-content', recursive=True)

    try:
        content = content_blk.get_text()
    except AttributeError as e:
        print(e)
        print('Content None')
        return None

    return content



#---------------Execution---------------#
if __name__ == '__main__':
    main()
