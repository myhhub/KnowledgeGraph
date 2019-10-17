#!/usr/bin/env python
# coding=utf-8


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import scrapy
from baidu_baike.items import BaiduBaikeItem
from bs4 import BeautifulSoup
import re
import urllib


class BaiduBaikeSpider(scrapy.Spider, object):
    # 定义爬虫名称
    name = 'baidu'
    # 设置允许的域，不以这个开头的链接不会爬取
    allowed_domains = ["baike.baidu.com"]
    # 爬虫开始的的网址
    start_urls = ['https://baike.baidu.com/item/%E5%88%98%E5%BE%B7%E5%8D%8E/114923']

    #start_urls = ['https://baike.baidu.com/item/%E4%B8%83%E5%B0%8F%E7%A6%8F']

    # 将返回的标签列表提取文本并返回
    def _get_from_findall(self, tag_list):
        result = []

        for slist in tag_list:
            tmp = slist.get_text()
            result.append(tmp)
        return result

    # 程序的核心，可以获取页面内的指定信息，并获取页面内的所有链接做进一步的爬取
    # response 是初始网址的返回
    def parse(self, response):
        # 分析 response来提取出页面最下部的标签信息，如果包含演员或电影则进行爬取，否则跳过
        page_category = response.xpath("//dd[@id='open-tag-item']/span[@class='taglist']/text()").extract()
        page_category = [l.strip() for l in page_category]
        item = BaiduBaikeItem()

        # tooooo ugly,,,, but can not use defaultdict
        for sub_item in ['actor_bio', 'actor_chName', 'actor_foreName', 'actor_nationality', 'actor_constellation',
                         'actor_birthPlace', 'actor_birthDay', 'actor_repWorks', 'actor_achiem', 'actor_brokerage',
                         'movie_bio', 'movie_chName', 'movie_foreName', 'movie_prodTime', 'movie_prodCompany',
                         'movie_director', 'movie_screenwriter', 'movie_genre', 'movie_star', 'movie_length',
                         'movie_rekeaseTime', 'movie_language', 'movie_achiem']:
            item[sub_item] = None

        # 如果包含演员标签则认为是演员
        if u'演员' in page_category:
            print("Get a actor page")
            soup = BeautifulSoup(response.text, 'lxml')
            summary_node = soup.find("div", class_="lemma-summary")
            item['actor_bio'] = summary_node.get_text().replace("\n", " ")

            # 使用 bs4 对页面内信息进行提取并保存到对应的item内
            all_basicInfo_Item = soup.find_all("dt", class_="basicInfo-item name")
            basic_item = self._get_from_findall(all_basicInfo_Item)
            basic_item = [s.strip() for s in basic_item]
            all_basicInfo_value = soup.find_all("dd", class_="basicInfo-item value")
            basic_value = self._get_from_findall(all_basicInfo_value)
            basic_value = [s.strip() for s in basic_value]
            for i, info in enumerate(basic_item):
                info = info.replace(u"\xa0", "")
                if info == u'中文名':
                    item['actor_chName'] = basic_value[i]
                elif info == u'外文名':
                    item['actor_foreName'] = basic_value[i]
                elif info == u'国籍':
                    item['actor_nationality'] = basic_value[i]
                elif info == u'星座':
                    item['actor_constellation'] = basic_value[i]
                elif info == u'出生地':
                    item['actor_birthPlace'] = basic_value[i]
                elif info == u'出生日期':
                    item['actor_birthDay'] = basic_value[i]
                elif info == u'代表作品':
                    item['actor_repWorks'] = basic_value[i]
                elif info == u'主要成就':
                    item['actor_achiem'] = basic_value[i]
                elif info == u'经纪公司':
                    item['actor_brokerage'] = basic_value[i]
            yield item
        elif u'电影' in page_category:
            print("Get a movie page!!")

            # 使用 bs4 对页面内的链接进行提取，而后进行循环爬取
            soup = BeautifulSoup(response.text, 'lxml')
            summary_node = soup.find("div", class_="lemma-summary")
            item['movie_bio'] = summary_node.get_text().replace("\n", " ")
            all_basicInfo_Item = soup.find_all("dt", class_="basicInfo-item name")
            basic_item = self._get_from_findall(all_basicInfo_Item)
            basic_item = [s.strip() for s in basic_item]
            all_basicInfo_value = soup.find_all("dd", class_="basicInfo-item value")
            basic_value = self._get_from_findall(all_basicInfo_value)
            basic_value = [s.strip() for s in basic_value]
            for i, info in enumerate(basic_item):
                info = info.replace(u"\xa0", "")
                if info == u'中文名':
                    item['movie_chName'] = basic_value[i]
                elif info == u'外文名':
                    item['movie_foreName'] = basic_value[i]
                elif info == u'出品时间':
                    item['movie_prodTime'] = basic_value[i]
                elif info == u'出品公司':
                    item['movie_prodCompany'] = basic_value[i]
                elif info == u'导演':
                    item['movie_director'] = basic_value[i]
                elif info == u'编剧':
                    item['movie_screenwriter'] = basic_value[i]
                elif info == u'类型':
                    item['movie_genre'] = basic_value[i]
                elif info == u'主演':
                    item['movie_star'] = basic_value[i]
                elif info == u'片长':
                    item['movie_length'] = basic_value[i]
                elif info == u'上映时间':
                    item['movie_rekeaseTime'] = basic_value[i]
                elif info == u'对白语言':
                    item['movie_language'] = basic_value[i]
                elif info == u'主要成就':
                    item['movie_achiem'] = basic_value[i]
            yield item

        soup = BeautifulSoup(response.text, 'lxml')
        links = soup.find_all('a', href=re.compile(r"/item/"))
        for link in links:
            new_url = link["href"]
            new_full_url = urllib.parse.urljoin('https://baike.baidu.com/', new_url)
            yield scrapy.Request(new_full_url, callback=self.parse)
