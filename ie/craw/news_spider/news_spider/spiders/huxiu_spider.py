#!/usr/bin/env python
# coding=utf-8

import scrapy
from news_spider.items import NewsSpiderItem

class HuxiuSpider(scrapy.Spider):
    name = "huxiu"
    allowed_domains = ["huxiu.com"]
    start_urls = ["http://www.huxiu.com"]


    def parse(self, response):

        print "Start............................"
        self.desc = ''
        for sel in response.xpath('//div[@class="mod-b mod-art clearfix "]'):
            item = NewsSpiderItem()
            item['title'] = sel.xpath('./div/h2/a[@class="transition msubstr-row2"]/text()')[0].extract()
            self.desc =  sel.xpath('./div[@class="mob-ctt index-article-list-yh"]/div[@class="mob-sub"]/text()')[0].extract()
            link = sel.xpath('./div/h2/a/@href')[0].extract()
            url = response.urljoin(link)

            yield scrapy.Request(url, callback=self.parse_article )

    def parse_article(self, response):
        detail = response.xpath('//div[@class="article-wrap"]')
        item = NewsSpiderItem()
        item['title'] =  detail.xpath('./h1[@class="t-h1"]/text()')[0].extract()
        item['auth'] = u"作者：" + detail.xpath('./div/span[@class="author-name"]/a/text()')[0].extract()
        item['post_time'] = u"发表时间：" + detail.xpath('./div/div[@class="column-link-box"]/span[@class="article-time pull-left"]/text()')[0].extract()
        item['descr'] = u"简述：" + self.desc + "\n"  # 简述存在错误
        all_pars = detail.xpath('//div[@class="article-content-wrap"]//p/text()').extract()
    
        content = ''
        for par in all_pars:
            content = content + par + "\n"

        desc = item.get('main_news')
        if desc == None:
            item['main_news'] = content
        else:
            item['main_news'] = desc + content

        yield item


