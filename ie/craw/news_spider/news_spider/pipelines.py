# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class NewsSpiderPipeline(object):
    
    def process_item(self, item, spider):
        self.news = open("./news/" + item["title"].strip()+ item["post_time"] + ".txt", "w")
        self.news.write(item["title"].encode("utf-8") + "\n")
        self.news.write(item["auth"].encode("utf-8") + "\n")
        self.news.write(item["post_time"].encode("utf-8") + "\n")
        self.news.write(item["descr"].encode("utf-8") + "\n")
        self.news.write(item["main_news"].encode("utf-8") + "\n")

        return item


    def spider_closed(self):
        self.news.close()
