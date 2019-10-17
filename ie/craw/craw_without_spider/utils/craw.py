#!/usr/bin/env python
# coding=utf-8

import chardet # for test

from bs4 import BeautifulSoup
import re
import urlparse
import urllib2
import sys, os
import pymysql
import basic_info
import httplib

httplib.HTTPConnection._http_vsn = 10  
httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0' # 强制指定HTTP/1.0

actor = u'\n\u6f14\u5458\n' # 演员的unicode 码,下面是电影的
movie = u'\n\u7535\u5f71\n'
global current_url

basic_attr = {}
basic_list = []
target = sys.argv[1]
if target == 'actor':
    target = actor
    insert_command = basic_info.insert_actor_command
    basic_attr = basic_info.actor_attr
    basic_list = basic_info.actor_info
elif target == 'movie':
    target = movie
    insert_command = basic_info.insert_movie_command
    basic_attr = basic_info.movie_attr
    basic_list = basic_info.movie_info

mysql_db = pymysql.connect(host="localhost", user="root", passwd='nlp', db="kg_movie", use_unicode=True, charset="utf8mb4")
mysql_cursor = mysql_db.cursor()
    
# manage the url
class UrlManager(object):
    def __init__(self):
        self.new_urls = self.get_old_urls("new_url.txt")
        self.old_urls = self.get_old_urls("old_url.txt")

    def get_old_urls(self, file):   # 从文件初始化已获取的网址列表
        with open(file, 'rw') as fo:
            ourls = fo.readlines()
            ourls = set(ourls)
            fo.close()
        return ourls

    def add_new_url(self, url):
        if url is None:
            raise Exception
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            pass
        else:
            for url in urls:
                self.add_new_url(url)

    def has_new_url(self):
        return len(self.new_urls) != 0

    def get_new_url(self):
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

# HTL download
class HTMLDownloader(object):
    def download(self, url):
        if url is None:
            return None
        response = urllib2.urlopen(url.encode('utf-8'))
        if response.getcode() != 200:
            return None
        try:
            return response.read()
        except:
            return None

# HTML parser
class HTMLParser(object):
    def _get_new_urls(self, page_url, soup):
        new_urls = []

        links = soup.find_all('a', href=re.compile(r"/item/"))
        for link in links:
            new_url = link["href"]
            new_full_url = urlparse.urljoin(page_url, new_url)
            new_urls.append(new_full_url)
        return new_urls

    def _get_from_findall(self, tag_list):
        result = []
        
        for slist in tag_list:
            tmp = slist.get_text()
            result.append(tmp)
        return result

    def dict_to_list(self, basic):
        detail_list = list()
        #actor_info = basic.keys() # dict不能保证 key按照初始化时的顺序存储

        for tag in basic_list:
            detail_list.append(basic[tag])
        return tuple(detail_list)

    def _get_new_data(self, soup, count):
        basic = basic_attr
        
        open_tag = soup.find_all("span", class_ = "taglist")
        tag = self._get_from_findall(open_tag)

        if target in tag : 
            summary_node = soup.find("div", class_ = "lemma-summary")
            basic[u'简介'] = summary_node.get_text().replace("\n"," ")
            basic['id'] = count
            
            basic_node = soup.find("div", class_ = "basic-info cmn-clearfix")
            all_basicInfo_item = soup.find_all("dt", class_ = "basicInfo-item name" )
            basic_item = self._get_from_findall(all_basicInfo_item)
            basic_item = [s.strip() for s in basic_item]
            all_basicInfo_value = soup.find_all("dd", class_ = "basicInfo-item value" )
            basic_value = self._get_from_findall(all_basicInfo_value)
            basic_value = [s.strip() for s in basic_value]

            for i, item in enumerate(basic_item):
                if basic.has_key(item.replace(u" ", "")):
                    basic[item.replace(u" ", "")] = basic_value[i].replace("\n","")
            count = count + 1
            
            print "检测到新目标，目前共采集总数： ", count - 1 

            return basic, count
        else:
            return None, count

    def parse(self, page_url, HTML_cont, count):
        if page_url is None or HTML_cont is None:
            return None, None, count

        soup = BeautifulSoup(HTML_cont, "html.parser", from_encoding="utf-8")
        print "目前正在处理的网页链接为: ", page_url
        new_urls = self._get_new_urls(page_url, soup)
        new_data, count = self._get_new_data(soup, count)
        return new_urls, new_data, count

class HTMLOutputer(object):
    def collect_data(self, data, count_er_id):
        if data is None:
            return count_er_id
        if sys.argv[1] == 'actor':
            count_er_id = self.get_actor_movie(data, count_er_id)
        elif sys.argv[1] == 'movie':
            count_er_id = self.get_movie_genre(data, count_er_id)
        data = HTMLParser.dict_to_list(data)
        try:
            mysql_cursor.execute(insert_command, data) # 将获得的数据插入到Mysql数据库中
            if count_er_id % 10 == 0:
                mysql_db.commit()
        except:
            print "Collect_data Warning: skiping this event due to some error: ", count_er_id

        return count_er_id

    def get_actor_movie(self, data, count_actor_movie):

        if data is None:
            return count_er_id
        pres = data[u'代表作品'].strip()
        pres = re.split(u'[，、]', pres)
        actor_id = data['id']
        
        for pre in pres:
            mysql_cursor.execute(basic_info.search_movie_id % pre )
            movie_id = mysql_cursor.fetchall()
            if movie_id:
                movie_id = movie_id[0][0]
                count_actor_movie = count_actor_movie + 1
                try:
                    mysql_cursor.execute(basic_info.insert_actor_movie_command, (count_actor_movie, actor_id, movie_id ))
                except:
                    print "Actor_Movie Warning: skip this duplicate event ", count_actor_movie, actor_id, movie_id

        return count_actor_movie

    def get_movie_genre(self, data, count_movie_genre):
        if data[u'类型'] is None:
            return count_movie_genre

        pres = data[u'类型'].strip()
        pres = re.split(u'[，、；]', pres)
        movie_id = data['id']

        for pre in pres:
            if pre in basic_info.movie_genre.keys():
                genre_id = basic_info.movie_genre[pre]
            else:
                genre_id = basic_info.movie_genre[u'其他']
            count_movie_genre = count_movie_genre + 1
            try:
                mysql_cursor.execute(basic_info.insert_movie_genre_command, (count_movie_genre, movie_id, genre_id ))
            except:
                print "Movie_Genre Warning: skip this duplicate event ", count_movie_genre, movie_id, genre_id 

        return count_movie_genre
            

class SpiderMain():
    def craw(self, root_url, page_counts):
        count = 1
        count_er_id = 0
        if sys.argv[1] == 'actor':
            count_er_id = mysql_cursor.execute( basic_info.get_largest_amid)
        elif sys.argv[1] == 'movie':
            count_er_id = mysql_cursor.execute( basic_info.get_largest_mgid)
        UrlManager.add_new_url(root_url)
        while UrlManager.has_new_url(): # still has url
            new_url =UrlManager.get_new_url()
            HTML_cont =HTMLDownloader.download(new_url)
            new_urls, new_data, count = HTMLParser.parse(new_url, HTML_cont, count)
            UrlManager.add_new_urls(new_urls)
            count_er_id = HTMLOutputer.collect_data(new_data, count_er_id)
            if count_er_id % 10 == 0:
                self.save_file("old_url.txt", UrlManager.old_urls)
                self.save_file("new_url.txt", UrlManager.new_urls)
            if count == page_counts+1:
                break
    
    def save_file(self, file, data):
        with open(file, "w") as wfile:
            wfile.write(str(data))
            wfile.close()

if __name__=="__main__":
    mysql_cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    print "\n欢迎使用百度百科爬虫,初始化中.... "
    UrlManager = UrlManager()
    HTMLDownloader = HTMLDownloader()
    HTMLParser = HTMLParser()
    HTMLOutputer = HTMLOutputer()

    root_url = "https://baike.baidu.com/item/%E5%BC%A0%E6%B6%B5%E4%BA%88"  #爬虫入口，默认是张涵予百科主页
    page_counts = input("输入想要爬取的目标数量:" )  #想要爬取的数量,没爬取到目标分类下的不计数
    SpiderMain = SpiderMain()

    print "\n开始爬取...."
    SpiderMain.craw(root_url,page_counts)   #启动爬虫

    #提交所有的insert 操作
    mysql_cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    mysql_db.commit()
    mysql_cursor.close()
    mysql_db.close()

