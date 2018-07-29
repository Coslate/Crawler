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
        One can input the parameter -url {url} to scrape the information from {url}
        One can input the parameter -isd {1/0} to get print out the debug messages
        One can input the parameter -cse {1/0} to consider keyword case sensitive
        One can input the parameter -thnum {threshold} to print out the article that keyword occurs {threshold} times
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
import time
import package_beauty.beauty as beauty

#########################
#     Main-Routine      #
#########################
def main():
    #test
    beauty.TestHello()


    #Disable Warning
    requests.packages.urllib3.disable_warnings()

    #Initial the month dictionary
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
    (start_time, end_time, keyword, out_dir, url, is_debug, case_sensitive, thresh_occur) = ArgumentParser(start_time)

    #Scraping all the related articles
    articles_dic_arr = GetAllThePages(start_time, end_time, keyword, url, month_dic, is_debug, out_dir, case_sensitive, thresh_occur)

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
    url             = "https://www.ptt.cc/bbs/nba/index.html"
    case_sensitive  = 0
    thresh_occur    = 0

    parser = argparse.ArgumentParser()
    parser.add_argument("--start_time", "-st", help="set the start time of searching articles")
    parser.add_argument("--end_time", "-et", help="set the end time of searching articles")
    parser.add_argument("--keyword", "-key", help="set the keyword that the content of an article will include and be searched")
    parser.add_argument("--out_dir", "-out", help="set the output directory to write out the articles")
    parser.add_argument("--url", "-url", help="set the url which will be scraped from")
    parser.add_argument("--is_debug", "-isd", help="set 1 to check the debug messages")
    parser.add_argument("--case_sensitive", "-cse", help="set 1 to use case sensitive when check the keyword")
    parser.add_argument("--thresh_occur", "-thnum", help="the threshold of the number that a keyword must occurs in an article for printing.")

    args = parser.parse_args()

    if args.start_time:
        start_time = int(args.start_time)
    if args.end_time:
        end_time = int(args.end_time)
    if args.keyword:
        keyword = args.keyword
    if args.out_dir:
        out_dir = args.out_dir
    if args.url:
        url = args.url
    if args.is_debug:
        is_debug = int(args.is_debug)
    if args.case_sensitive:
        case_sensitive = int(args.case_sensitive)
    if args.thresh_occur:
        thresh_occur = int(args.thresh_occur)

    if(is_debug > 0):
        is_debug = True
    else:
        is_debug = False

    return (start_time, end_time, keyword, out_dir, url, is_debug, case_sensitive, thresh_occur)

def GetStrValue(tag, numeric_if_none):
    if(tag == None):
        if(numeric_if_none):
            return 0
        else:
            return "None"
    else:
        return tag.get_text().strip()

def GetThePageAndUpdateURL(date_reform_prev, earlest_time, url, articles_dic_arr, start_time, end_time, month_dic, keyword, is_debug, out_dir, case_sensitive, thresh_occur):
    #--------------------------------------------------------------
    #Step1. Issue Request.
    #--------------------------------------------------------------
    response = None
    while(response is None):
        try:
            response = requests.get(url, cookies = {'over18':"1"}, verify = False)
        except HTTPError as e:
            print(e)
            sys.exit()
        except:
            print("Connection refused by the server..")
            print("Reconnected after 5 seconds")
            print("...")
            time.sleep(5)
            print("Continuing...")
            continue

    #--------------------------------------------------------------
    #Step2. Interpret Response with Beautifulsoup.
    #--------------------------------------------------------------

    soup         = BeautifulSoup(response.text, 'lxml')
    articles     = soup.find_all('div', {"class":"r-ent"})

    for article in articles:
        title_class = article.find('div', 'title').find('a') or BeautifulSoup('<a>本文已被刪除</a>', 'lxml').a
        title    = GetStrValue(title_class, 0)
        link     = title_class.get('href')
        push_num = GetStrValue(article.find('div', 'nrec').find('span', {"class":re.compile("^hl\s*.*")}), 1)
        date     = GetStrValue(article.find('div', 'meta').find('div', {"class":"date"}), 0)
        author   = GetStrValue(article.find('div', 'meta').find('div', {"class":"author"}), 0)

        if((title == "None") or (re.match(r'\s*\[\s*公告\s*\].*', title) is not None)):
            continue

        #Get the link_url to the content
        link_url    = urlparse.urljoin(url, link)

        #Get the detailed timing info of the content
        date_reform = GetTimeInfo(link_url, month_dic, start_time, is_debug)

        if((len(str(date_reform)) < 8) and (date_reform is not None)):
            if(earlest_time == 99999999):
                print(f'Warning : Get the date_reform = {date_reform} in the article -> ')
                print(f"Warning : title_f = {title}")
                print(f"Warning : push_num_f = {push_num}")
                print(f"Warning : author_f = {author}")
                print(f"Warning : date_f = {date}")
                print(f"Warning : link_url_f = {link_url}")
                continue
            else:
                time_match = re.match(r'(\d+)(\d)(\d)(\d)(\d)', date_reform_prev)
                if(time_match is not None):
                    month_prev = str(time_match.group(2))+str(time_match.group(3))
                    dat_prev = str(time_match.group(4))+str(time_match.group(5))
                    year_prev = str(time_match.group(1))

                    time_match_curr = re.match(r'(\d+)/(\d+)', date)
                    if(time_match_curr is not None):
                        month_curr = str(time_match_curr.group(1)).zfill(2)
                        day_curr = str(time_match_curr.group(2)).zfill(2)

                        if(month_prev == month_curr):
                            date_reform = str(year_prev)+str(month_curr)+str(day_curr)
                        elif(int(month_curr) > int(month_prev)):
                            date_reform = str(year_prev)+str(month_curr)+str(day_curr)
                        else:
                            date_reform = str((int(year_prev)-1))+str(month_curr)+str(day_curr)
                    else:
                        date_reform = date_reform_prev
                        print(f'Warning : date is not match the x/y format. Please check the article -> ')
                        print(f"Warning : title_f = {title}")
                        print(f"Warning : push_num_f = {push_num}")
                        print(f"Warning : author_f = {author}")
                        print(f"Warning : date_f = {date}")
                        print(f"Warning : link_url_f = {link_url}")
                else:
                    date_reform = None

        if(date_reform == None):
            continue

        date_reform_prev = date_reform
        if(int(date_reform) < earlest_time):
            title_match1 = re.match(r'.*NBA\s*Playoffs\s*圖表.*賽程.*轉播\s*', title)
            title_match2 = re.match(r'\s*\[\s*活動\s*\]\s*ＮＢＡ之年度徵文大賞\s*', title)
            if((title_match1 is None) and (title_match2 is None)):
                earlest_time = int(date_reform)

                if(is_debug):
                    print(f"<====================================>")
                    print(f"earlest_time update...{earlest_time}")
                    print(f"title = {title}")
                    print(f"link_url = {link_url}")
                    print(f"author = {author}")
                    print(f"date = {date}")
                    print(f"push_num = {push_num}")

        if((int(date_reform) <= int(start_time)) and (int(date_reform) >= int(end_time))):
            #Get the content
            content_info   = GetContentInfo(link_url)
            if(content_info == None):
                continue

            if(keyword == None):
                articles_dic_arr.append({"title":title, "link":link_url, "push_num":push_num, "date":date, "author":author, "date_reform":date_reform, "content_info":content_info})
                ProcessTitleWriteOutFile(title, date_reform, author, push_num, out_dir, content_info)
                if(is_debug):
                    print(f"============================")
                    print(f"Get article without keyword!")
                    print(f"title = {title}")
                    print(f"push_num = {push_num}")
                    print(f"author = {author}")
                    print(f"date = {date}")
                    print(f"date_reform = {date_reform}")
                    print(f"link_url = {link_url}")

            else:
                str_line_arr   = content_info.split('\n')
                title_line_arr = title.split('\n')
                l_cnt       = [CheckLineIncludesKeywords(keyword, line, case_sensitive) for line in str_line_arr]
                l_cnt_title = [CheckLineIncludesKeywords(keyword, line, case_sensitive) for line in title_line_arr]

                if((sum(l_cnt) > thresh_occur) or (sum(l_cnt_title) > thresh_occur)):
                    #Store all the information
                    articles_dic_arr.append({"title":title, "link":link_url, "push_num":push_num, "date":date, "author":author, "date_reform":date_reform, "content_info":content_info})
                    ProcessTitleWriteOutFile(title, date_reform, author, push_num, out_dir, content_info)

                if(is_debug):
                    print(f"============================")
                    print(f"Get article with keyword!")
                    print(f"l_cnt = {l_cnt}")
                    print(f"l_cnt_title = {l_cnt_title}")
                    print(f"title = {title}")
                    print(f"push_num = {push_num}")
                    print(f"author = {author}")
                    print(f"date = {date}")
                    print(f"date_reform = {date_reform}")

    #--------------------------------------------------------------
    #Step3. Find the URL of Previous Pages.
    #--------------------------------------------------------------
    link_url = soup.find("div", {"class":re.compile("^btn\-group\s*btn\-group\-paging$")}).find("a", {"class":"btn wide"}, text=re.compile("上頁"))["href"]
    link_url = urlparse.urljoin(url, link_url)

    if(is_debug):
        print(f'================================')
        print(f'=====index_url = {link_url}=====')
        print(f'================================')

    return (link_url, earlest_time, date_reform_prev)

def GetAllThePages(start_time, end_time, keyword, url, month_dic, is_debug, out_dir, case_sensitive, thresh_occur):
    articles_dic_arr = []
    count_once = 0
    earlest_time = 99999999
    date_reform_prev = 0

    while(True):
        this_loop_article = []
        (url, earlest_time, date_reform_prev) = GetThePageAndUpdateURL(date_reform_prev, earlest_time, url, this_loop_article, start_time, end_time, month_dic, keyword, is_debug, out_dir, case_sensitive, thresh_occur)
        if(is_debug):
            print(f'earlest_time of this link_url page= {earlest_time}')
        for each_article in this_loop_article:
            articles_dic_arr.append((each_article))
        if(count_once < 2):
            count_once += 1
        if((int(earlest_time) < int(end_time)) and (count_once > 1)):
            print(f'earlest_time <break>= {earlest_time}')
            break

    return (articles_dic_arr)

def GetTimeInfo(link_url, month_dic, start_time, is_debug):
    response = None
    while(response is None):
        try:
            response = requests.get(link_url, verify = False)
        except HTTPError as e:
            print(e)
            sys.exit()
        except:
            print("Connection refused by the server..")
            print("Reconnected after 5 seconds")
            time.sleep(5)
            print("Continuing...")
            continue

    soup = BeautifulSoup(response.text, 'lxml')

    try:
        time_blk = soup.find('span', 'article-meta-value', text=re.compile("^\S+\s+(\S+)\s+(\S+)\s+\S+\:\S+\:\S+\s+(\S+)\s*")).get_text()
        time_match = re.match(r"^\S+\s*(\S+)\s*(\S+)\s*\S+\:\S+\:\S+\s*(\S+)\s*", time_blk)
        month = month_dic[time_match.group(1)]
        year  = int(time_match.group(3))
        day   = "{:02d}".format(int(time_match.group(2)))
    except AttributeError as e:
        try:
            time_blk = soup.find('span', 'f2', text=re.compile("※\s*編輯:\s*.*,\s*\d*/\d*/\d*\s*\S+:\S+:\S+\s*")).get_text()
            time_match = re.match(r"※\s*編輯:\s*.*,\s*(\d+)/(\d+)/(\d+)\s*\S+:\S+:\S+\s*", time_blk)
            month = int(time_match.group(1))
            year  = int(time_match.group(3))
            day   = "{:02d}".format(int(time_match.group(2)))
        except AttributeError as e:
            print(e)
            print('Warning : time_blk not found.')
            print('Warning : return None.')
            return None

    if(is_debug):
        print(f'time_blk ={time_blk}')

    return(str(year)+str(month)+str(day))

def GetContentInfo(link_url):
    payload = {
        "from" : "/bbs/Gossiping/index.html",
        "yes"  : "yes"
    }

    response = None
    while(response is None):
        try:
#           response = requests.get(link_url)
            rs = requests.session()
            res = rs.post("https://www.ptt.cc/ask/over18", verify = False, data = payload)
            response = rs.get(link_url, verify = False)
        except HTTPError as e:
            print(e)
            print('Respones None')
            sys.exit()
        except:
            print("Connection refused by the server..")
            print("Reconnected after 5 seconds")
            time.sleep(5)
            print("Continuing...")
            continue

    soup = BeautifulSoup(response.text, 'lxml')
    content_blk = soup.find('div', class_="bbs-screen bbs-content", id='main-content', recursive=True)

    try:
        content = content_blk.get_text()
    except AttributeError as e:
        print(e)
        print('Content None')
        return None

    return content

def ProcessTitleWriteOutFile(title, date_reform, author, push_num, out_dir, content_info):
    pattern = re.compile(r'\s*')
    title = re.sub(pattern, '', title)
    title = title.replace('[', '_')
    title = title.replace(']', '_')
    title = title.replace('/', '_')

    file_name = title+"_"+date_reform+"_"+author+'_'+str(push_num)+".txt"
    with open('{x}/{y}'.format(x = out_dir, y = file_name), 'w') as out_file:
        out_file.write(content_info)
    out_file.closed

def CheckLineIncludesKeywords(keyword, line, case_sensitive):
    included_num = 0
    keyword_arr = keyword.split('_')

    for keyword_element in keyword_arr:
        if(case_sensitive):
            included_num += len(re.findall(r'{x}'.format(x = keyword_element), line))
        else:
            included_num += len(re.findall(r'{x}'.format(x = keyword_element.lower()), line.lower()))

    return included_num

#---------------Execution---------------#
if __name__ == '__main__':
    main()
