# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pymysql
from pymysql import connections
from baidu_baike import settings


class BaiduBaikePipeline(object):
    def __init__(self):
        self.article_file = open("articles.txt", "a+",encoding='utf-8')

    def process_item(self, item, spider):
        # process info for actor
        articles = bytes.decode(str(item['articles']).encode('utf-8')).replace("\n", " ")
        article_id = bytes.decode(str(item['article_id']).encode('utf-8'))

        self.article_file.write(article_id + "," + articles + "\n")

    def close_spider(self, spider):
        self.article_file.close()
