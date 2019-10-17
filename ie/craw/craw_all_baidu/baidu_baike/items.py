# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaiduBaikeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    title_id = scrapy.Field()
    abstract = scrapy.Field()
    infobox = scrapy.Field()
    subject = scrapy.Field()
    disambi = scrapy.Field()
    redirect = scrapy.Field()
    curLink = scrapy.Field()
    interPic = scrapy.Field()
    interLink = scrapy.Field()
    exterLink = scrapy.Field()
    relateLemma = scrapy.Field()
    all_text = scrapy.Field()
