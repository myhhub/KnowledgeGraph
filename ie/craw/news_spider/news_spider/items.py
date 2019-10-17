# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()     # 标题
    descr = scrapy.Field()     # 简述
    auth = scrapy.Field()      # 作者
    post_time = scrapy.Field() # 发布时间
    main_news = scrapy.Field() # 新闻内容
