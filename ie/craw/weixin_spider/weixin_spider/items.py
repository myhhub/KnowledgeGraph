# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeixinSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()       # 文章标题
    publishTime = scrapy.Field() # 发布时间
    publicName = scrapy.Field()  # 公众号名字
    article = scrapy.Field()     # 文章内容
    cite = scrapy.Field()        # 文章引用来源
