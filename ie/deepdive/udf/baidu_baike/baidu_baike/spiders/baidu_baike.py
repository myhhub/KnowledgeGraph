#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import
from __future__ import division     
from __future__ import print_function


from baidu_baike.items import BaiduBaikeItem
import scrapy
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import urllib

class BaiduBaikeSpider(scrapy.Spider, object):
    name = 'baidu'
    allowed_domains = ["baike.baidu.com"]
    start_urls = ['https://baike.baidu.com/item/%E5%91%A8%E6%98%9F%E9%A9%B0/169917?fr=aladdin']
    global article_id
    article_id = 0
#    start_urls = ['https://baike.baidu.com/item/%E4%B8%83%E5%B0%8F%E7%A6%8F']
    
    def _get_from_findall(self, tag_list):
        result = []        
                           
        for slist in tag_list:
            tmp = slist.get_text()
            result.append(tmp)
        return result

    def parse(self, response):
        global article_id
        page_category = response.xpath("//dd[@id='open-tag-item']/span[@class='taglist']/text()").extract()
        page_category = [l.strip() for l in page_category]
        item = BaiduBaikeItem()

        item['article_id'] = article_id
        item['articles'] = ''

        if u'演员' in page_category or u'电影' in page_category:
            print("Get a actor/movie page")
            soup = BeautifulSoup(response.text, 'lxml')
            root_node = soup.find("div", class_ = "main_tab main_tab-defaultTab curTab")

            para_nodes = soup.find_all("div", class_="para")
            basic_item = self._get_from_findall(para_nodes)
            article_content = ' '.join(basic_item)
            article_content = article_content.replace("\n", " ")
            item['articles'] = str(article_content)
            article_id += 1
            yield item
            if article_id % 50 == 0:
                print("The nums of total articles up to: {}".format(article_id))


        soup = BeautifulSoup(response.text, 'lxml')
        links = soup.find_all('a', href=re.compile(r"/item/"))
        for link in links:
            new_url = link["href"]
            new_full_url = urllib.parse.urljoin('https://baike.baidu.com/', new_url)
            yield scrapy.Request(new_full_url, callback=self.parse)
