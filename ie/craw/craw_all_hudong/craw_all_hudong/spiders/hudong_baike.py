#!/usr/bin/env python2.7
# coding=utf-8

from __future__ import absolute_import
from __future__ import division     
from __future__ import print_function


from craw_all_hudong.items import CrawAllHudongItem
from scrapy.utils.log import configure_logging
import scrapy
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
import urlparse
import json

strong = re.compile(r".*?<strong>(.*?)</strong>.*?")
span = re.compile(r".*?<span>(.*?)</span>.*?")
hr = re.compile(r"<a href.*?/a>")

class CrawAllHudongSpider(scrapy.Spider, object):
    name = 'hudong'
    allowed_domains = ["baike.com"]
#    start_urls = ['http://www.baike.com/wiki/%E4%B8%8A%E6%B5%B7%E5%B8%82'] # 上海
#    start_urls = ['http://www.baike.com/wiki/%E6%82%AC%E5%B4%96%E7%A7%8B%E5%8D%83&prd=resoukuang'] # 星爷
#    start_urls = ['http://so.baike.com/doc/%E7%BB%B3%E5%AD%90'] # 星爷
#    start_urls = ['http://fenlei.baike.com/%E7%A7%91%E5%AD%A6/?prd=shouye_erjidaohang_fenleidaohang']
#    start_urls = ['http://fenlei.baike.com/%E7%94%B7%E6%BC%94%E5%91%98/?prd=zhengwenye_left_kaifangfenlei']
    start_urls = ['http://fenlei.baike.com/%E9%A1%B5%E9%9D%A2%E6%80%BB%E5%88%86%E7%B1%BB']
    
    def _get_from_findall(self, tag_list):
        result = []        
        for slist in tag_list:
            tmp = slist.get_text()
            result.append(tmp)
        return result

    def parse(self, response):
        # tooooo ugly,,,, but can not use defaultdict
        if response.url.find("www.baike.com") != -1:
            item = CrawAllHudongItem()
            for sub_item in [ 'title', 'title_id', 'abstract', 'infobox', 'subject', 'disambi', 'redirect', 'curLink', 'interPic', 'interLink', 'exterLink', 'relateLemma']:
                item[sub_item] = None
    
            disambi = response.xpath("//div[@class='content-h1']/h1/text()").extract()
            title = ' '.join(disambi).split("[")[0]
    #        redirect_name = response.xpath("//p[@id='unifypromptone']/a/text()").extract()
            redirect_line = response.xpath("//p[@id='unifypromptone']/a/text()").extract()
    #        print("redirect_line: ", type(redirect_line), redirect_line)
            if len(redirect_line) not in [0, 2]:
                print("Multi redirect name({}) found in lemmas: {}".format(len(redirect_line), title))
            try:
                redirect_name = redirect_line[0] if redirect_line[0] != disambi else redirect_line[1]
            except:
                redirect_name = None
            try:
                item['title'] = title
            except:
                item['title'] = None
            try:
                item['disambi'] = ''.join(disambi)
            except:
                item['disambi'] = None
            try:
                item['redirect'] = ''.join(redirect_name)
            except:
                item['redirect'] = None
            try:
                item['curLink'] = str(response.url)
            except:
                item['curLink'] = None
    
            soup = BeautifulSoup(response.text, 'lxml')
            summary_node = soup.find("div", class_ = "summary")
            try:
                item['abstract'] = summary_node.get_text().replace("\n"," ")
            except:
                item['abstract'] = None
    
            page_category = response.xpath("//dl[@id='show_tag']/dd[@class='h27']/a/text()").extract()
            page_category = [l.strip() for l in page_category]
            try:
                item['subject'] = ','.join(page_category)
            except:
                item['subject'] = None
            sameas_lemma = response.xpath("//dl[@id='show_thesaurus']/dd[@class='h27']/a/text()").extract()
            sameas_link = response.xpath("//dl[@id='show_thesaurus']/dd[@class='h27']/a/@href").extract()
            sameas_link = ['http://www.baike.com' + l  if not l.startswith("http") else l for l in sameas_link]
            relateLemma = {k:v for k,v in zip(sameas_lemma, sameas_link)}
            relateLemma = json.dumps(relateLemma)
            try:
                item['relateLemma'] = relateLemma
            except:
                item['relateLemma'] = None
    
            # Get infobox
    #        all_info_key =  response.xpath("//div[@id='datamodule']/div[@class='module zoom']/table/tbody/tr/td/strong/text()").extract()
    #        all_value_key =  response.xpath("//div[@id='datamodule']/div[@class='module zoom']/table/tbody/tr/td/span").extract()
            raw_info =  response.xpath("//div[@id='datamodule']/div[@class='module zoom']/table/tbody/tr/td").extract()
            info_dict = {}
            for each_item in raw_info:
                    k = re.findall(strong, each_item)
                    if len(k) == 0 : continue
                    k = " ".join(k) if len(k) > 1 else str(k[0])
                    v = re.findall(span, each_item)
                    v = [re.sub(hr, "", i) for i in v]
                    info_dict[k] = v
    
            try:
                item['infobox'] = json.dumps(info_dict)
            except:
                item['infobox'] = None
           
            # Get inter picture
            selector = scrapy.Selector(response)
            img_path = selector.xpath("//img/@src").extract()
            try:
                item['interPic'] = ','.join(img_path)
            except:
                item['interPic'] = None
    
            inter_links_dict = {}
            inter_links = response.xpath("//a[@class='innerlink']/@href").extract()
            inter_links_title = response.xpath("//a[@class='innerlink']/text()").extract()
            if len(inter_links) != len(inter_links_title):
                inter_links_title = ["None"+i for i in range(len(inter_links))]
            for link, link_text in zip(inter_links, inter_links_title):
                if not link.startswith("http"):
                    link = urlparse.urljoin('http://www.baike.com/', link)
                inter_links_dict[link_text] = link
            try:
                item['interLink'] = json.dumps(inter_links_dict)
            except:
                item['interLink'] = None
            
            exter_links_dict = {}
    #        soup = BeautifulSoup(response.text, 'lxml')
    #        exterLink_links = soup.find_all('a', href=re.compile(r"/redirect/"))
            exterLink_links = response.xpath("//div[@class='relevantinfo']/a[@href='javascript:void(0)']/@onclick").extract()
            exterLink_links_text = response.xpath("//div[@class='relevantinfo']/a[@href='javascript:void(0)']/text()").extract()
            if len(exterLink_links) != len(exterLink_links_text):
                exterLink_links_text = ["None"+i for i in range(len(exterLink_links))]
            for link, link_title in zip(exterLink_links, exterLink_links_text):
                exter_links_dict[link_title] = link
            try:
                item['exterLink'] = json.dumps(exter_links_dict)
            except:
                item['exterLink'] = None
    
            all_para = soup.find_all('div',id="content")
            all_text = [para.get_text() for para in all_para]
            try:
                item['all_text'] = ' '.join(all_text)
            except:
                item['all_text'] = None
    
            yield item

#        soup = BeautifulSoup(response.text, 'lxml')
#        links = soup.find_all('a', href=re.compile(r"/item/"))
        seen_links = []
        if response.url.find("so.baike") != -1:
            result_list = response.xpath("//div[@class='result-list']/h3/a/@href").extract()
        elif response.url.find("www.baike.com") != -1:
            result_list = response.xpath("//a[@class='innerlink']/@href").extract()
        elif response.url.find("baike") != -1:
            result_list = response.xpath("//a/@href").extract()
        seen_links.extend(result_list)

        for link in seen_links:
            if link.startswith("/wiki"):
                link = urlparse.urljoin('http://www.baike.com/', link)
            if link.find("baike") == -1:
                continue
#            print("@"*10, "link: ", link)
            yield scrapy.Request(link, callback=self.parse)
