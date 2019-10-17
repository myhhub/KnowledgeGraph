#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import
from __future__ import division     
from __future__ import print_function


from hudong_baike.items import HudongBaikeItem
import scrapy
from scrapy.http import Request
from bs4 import BeautifulSoup
import re

class HudongBaikeSpider(scrapy.Spider, object):
    name = 'hudong'
    allowed_domains = ["www.baike.com"]
    #start_urls = ['http://www.baike.com/wiki/%E5%94%90%E4%BC%AF%E8%99%8E%E7%82%B9%E7%A7%8B%E9%A6%99'] # tangbohu
    start_urls = ['http://www.baike.com/wiki/%E5%91%A8%E6%98%9F%E9%A9%B0&prd=button_doc_entry'] # zhouxingchi
    #start_urls = ['http://www.baike.com/wiki/%E6%9C%B1%E4%B8%80%E9%BE%99'] # zhouxingchi
    
    def _get_from_findall(self, tag_list):
        result = []        
                           
        for slist in tag_list:
            tmp = slist.get_text()
            result.append(tmp)
        return result

    def parse(self, response):
        page_category = response.xpath('//dl[@id="show_tag"]/dd[@class="h27"]/a/text()').extract()
        page_category = [l.strip() for l in page_category]
        item = HudongBaikeItem()

        # tooooo ugly,,,, but can not use defaultdict
        for sub_item in [ 'actor_bio', 'actor_chName', 'actor_foreName', 'actor_nationality', 'actor_constellation', 'actor_birthPlace', 'actor_birthDay', 'actor_repWorks', 'actor_achiem', 'actor_brokerage','movie_bio', 'movie_chName', 'movie_foreName', 'movie_prodTime', 'movie_prodCompany', 'movie_director', 'movie_screenwriter', 'movie_genre', 'movie_star', 'movie_length', 'movie_rekeaseTime', 'movie_language', 'movie_achiem' ]:
            item[sub_item] = None

        if u'演员' in page_category:
            print("Get a actor page")
            soup = BeautifulSoup(response.text, 'lxml')
            summary_node = soup.find("div", class_ = "summary")
            item['actor_bio'] = summary_node.get_text().replace("\n"," ")
            basic_item = []
            basic_value = []

            all_tds = response.xpath('//div[@class="module zoom"]//td').extract()
            for each_td in all_tds:
                strong_span = each_td.split("</td>")[0].split("</strong>")
                for sub_strong_span in strong_span:
                    if sub_strong_span.find("<strong>") != -1:
                        get_strong = sub_strong_span.split("<strong>")[-1]
                        basic_item.append(get_strong)
                    elif sub_strong_span.find("<span>") != -1:
                        get_span = sub_strong_span.split("</span>")
                        total_span = ''
                        for each_span in get_span:
                            each_span = each_span.strip("\n *<span>")
                            if each_span != '':
                                # remove all html tags in item & value
                                if each_span.find("href") != -1:
                                    each_span = re.sub(r'<a href=.*_blank">', "", each_span)
                                    each_span = re.sub(r'href.*blank"', "", each_span)
                                    each_span = re.sub(r'<img.*png">', "", each_span)
                                    each_span = re.sub(r'</a>', "", each_span)
                                    each_span = re.sub(r'[</>]', "", each_span)
                                total_span = total_span + " " + each_span
                        basic_value.append(total_span)

            for i, info in enumerate(basic_item):
                info = info.replace(u"\xa0", "")
                info = info.replace(u"\uff1a", "")
                if info == u'中文名':
                    item['actor_chName'] = basic_value[i]
                elif info == u'英文名':
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

            soup = BeautifulSoup(response.text, 'lxml')
            summary_node = soup.find("div", class_ = "summary")
            item['movie_bio'] = summary_node.get_text().replace("\n"," ")
            basic_item = []
            basic_value = []

            all_tds = response.xpath('//div[@class="module zoom"]//td').extract()
            for each_td in all_tds:
                strong_span = each_td.split("</td>")[0].split("</strong>")
                for sub_strong_span in strong_span:
                    if sub_strong_span.find("<strong>") != -1:
                        get_strong = sub_strong_span.split("<strong>")[-1]
                        basic_item.append(get_strong)
                    elif sub_strong_span.find("<span>") != -1:
                        get_span = sub_strong_span.split("</span>")
                        total_span = ''
                        for each_span in get_span:
                            each_span = each_span.strip("\n *<span>")
                            if each_span != '':
                                # remove all html tags in item & value
                                if each_span.find("href") != -1:
                                    each_span = re.sub(r'<a href=.*_blank">', "", each_span)
                                    each_span = re.sub(r'href.*blank"', "", each_span)
                                    each_span = re.sub(r'<img.*png">', "", each_span)
                                    each_span = re.sub(r'</a>', "", each_span)
                                    each_span = re.sub(r'[</>]', "", each_span)
                                total_span = total_span + " " + each_span
                        basic_value.append(total_span)
                              
            for i, info in enumerate(basic_item):
                info = info.replace(u"\xa0", "")
                info = info.replace(u"\uff1a", "")
                if info == u'中文名':
                    item['movie_chName'] = basic_value[i]
                elif info in [u'外文名', u'别名'] :
                    item['movie_foreName'] = basic_value[i]
                elif info == u'出品时间':
                    item['movie_prodTime'] = basic_value[i]
                elif info == u'出品公司':
                    item['movie_prodCompany'] = basic_value[i]
                elif info == u'导演':
                    item['movie_director'] = basic_value[i]
                elif info == u'编剧':
                    item['movie_screenwriter'] = basic_value[i]
                elif info in [u'类型', u'类别']:
                    item['movie_genre'] = basic_value[i]
                elif info == u'主演':
                    item['movie_star'] = basic_value[i]
                elif info == u'片长':
                    item['movie_length'] = basic_value[i]
                elif info == u'上映时间':
                    item['movie_rekeaseTime'] = basic_value[i].replace('title="" href=""', "")
                elif info == u'对白语言':
                    item['movie_language'] = basic_value[i]
                elif info == u'主要成就':
                    item['movie_achiem'] = basic_value[i]
            yield item

        new_urls = response.xpath("//a/@href").extract()
        for link in new_urls:
            if link.startswith('http://www.baike.com/wiki'):
                pass
                yield scrapy.Request(link, callback=self.parse)
