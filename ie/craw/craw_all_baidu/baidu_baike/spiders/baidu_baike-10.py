#!/usr/bin/env python2.7
# coding=utf-8

from __future__ import absolute_import
from __future__ import division     
from __future__ import print_function


from baidu_baike.items import BaiduBaikeItem
from scrapy.utils.log import configure_logging
import scrapy
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import urllib
import json

class BaiduBaikeSpider(scrapy.Spider, object):
    name = 'baidu10'
    allowed_domains = ["baike.baidu.com"]
    start_urls = ['https://baike.baidu.com/item/%E7%A7%92%E6%87%82%E7%9C%8B%E7%93%A6%E7%89%B9']
    
    def _get_from_findall(self, tag_list):
        result = []        
        for slist in tag_list:
            tmp = slist.get_text()
            result.append(tmp)
        return result

    def parse(self, response):
        # tooooo ugly,,,, but can not use defaultdict
        item = BaiduBaikeItem()
        for sub_item in [ 'title', 'title_id', 'abstract', 'infobox', 'subject', 'disambi', 'redirect', 'curLink', 'interPic', 'interLink', 'exterLink', 'relateLemma']:
            item[sub_item] = None

        mainTitle = response.xpath("//dd[@class='lemmaWgt-lemmaTitle-title']/h1/text()").extract()
        subTitle = response.xpath("//dd[@class='lemmaWgt-lemmaTitle-title']/h2/text()").extract()
        redirect_name = response.xpath("//span[@class='viewTip-fromTitle']/text()").extract()
        try:
            item['title'] = ' '.join(mainTitle)
        except:
            item['title'] = None
        try:
            item['disambi'] = ' '.join(mainTitle + subTitle)
        except:
            item['disambi'] = None
        try:
            item['redirect'] = ' '.join(redirect_name)
        except:
            item['redirect'] = None
        try:
            item['curLink'] = str(response.url)
        except:
            item['curLink'] = None

        soup = BeautifulSoup(response.text, 'lxml')
        summary_node = soup.find("div", class_ = "lemma-summary")
        try:
            item['abstract'] = summary_node.get_text().replace("\n"," ")
        except:
            item['abstract'] = None

        page_category = response.xpath("//dd[@id='open-tag-item']/span[@class='taglist']/text()").extract()
        page_category = [l.strip() for l in page_category]
        try:
            item['subject'] = ','.join(page_category)
        except:
            item['subject'] = None

        # Get infobox
        all_basicInfo_Item = soup.find_all("dt", class_="basicInfo-item name")
        basic_item = self._get_from_findall(all_basicInfo_Item)
        basic_item = [s.strip().replace('\n', ' ') for s in basic_item]
        all_basicInfo_value = soup.find_all("dd", class_ = "basicInfo-item value" )
        basic_value = self._get_from_findall(all_basicInfo_value)
        basic_value = [s.strip().replace(u'收起', '') for s in basic_value]
        info_dict = {}
        for i, info in enumerate(basic_item):
            info_dict[info] = basic_value[i]
        try:
            item['infobox'] = json.dumps(info_dict)
        except:
            item['infobox'] = None
       
        # Get inter picture
        selector = scrapy.Selector(response)
        img_path = selector.xpath("//img[@class='picture']/@src").extract()
        try:
            item['interPic'] = ','.join(img_path)
        except:
            item['interPic'] = None

        inter_links_dict = {}
        soup = BeautifulSoup(response.text, 'lxml')
        inter_links = soup.find_all('a', href=re.compile(r"/item/"))
        for link in inter_links:
            new_url = link["href"]
            url_name = link.get_text()
            new_full_url = urllib.parse.urljoin('https://baike.baidu.com/', new_url)
            inter_links_dict[url_name] = new_full_url
        try:
            item['interLink'] = json.dumps(inter_links_dict)
        except:
            item['interLink'] = None
        
        exter_links_dict = {}
        soup = BeautifulSoup(response.text, 'lxml')
        exterLink_links = soup.find_all('a', href=re.compile(r"/redirect/"))
        for link in exterLink_links:
            new_url = link["href"]
            url_name = link.get_text()
            new_full_url = urllib.parse.urljoin('https://baike.baidu.com/', new_url)
            exter_links_dict[url_name] = new_full_url
        try:
            item['exterLink'] = json.dumps(exter_links_dict)
        except:
            item['exterLink'] = None

        all_para = soup.find_all('div',class_="para")
        all_text = [para.get_text() for para in all_para]
        try:
            item['all_text'] = ' '.join(all_text)
        except:
            item['all_text'] = None

        yield item

        soup = BeautifulSoup(response.text, 'lxml')
        links = soup.find_all('a', href=re.compile(r"/item/"))
        for link in links:
            new_url = link["href"]
            new_full_url = urllib.parse.urljoin('https://baike.baidu.com/', new_url)
            yield scrapy.Request(new_full_url, callback=self.parse)
