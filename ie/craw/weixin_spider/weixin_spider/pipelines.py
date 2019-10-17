# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from pymysql import connections
from weixin_spider import  settings
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class WeixinSpiderPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(
            host=settings.HOST_IP,
#            port=settings.PORT,
            user=settings.USER,
            passwd=settings.PASSWD,
            db=settings.DB_NAME,
            charset='utf8mb4',
            use_unicode=True
            )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        title = str(item['title']).decode('utf-8')
        publishTime = str(item['publishTime']).decode('utf-8') 
        article = str(item['article']).decode('utf-8') 
        publicName = str(item['publicName']).decode('utf-8') 
        cite = str(item['cite']).decode('utf-8') 

        # 查询数据库，获取当前存在的文章标题，防止重复存入，但查表浪费时间
        self.cursor.execute("SELECT title FROM weixin_xiaoshuo;")
        titleList = self.cursor.fetchall()
        titleStr = ''.join(map(str, titleList))

        self.cursor.execute("SELECT publicName FROM weixin_xiaoshuo;")
        nameList = self.cursor.fetchall()
        nameStr = ''.join(map(str, nameList))

        if titleStr.find(title) == -1 and nameStr.find(publicName) == -1:
            # 执行SQL插入语句
            sql = """
            INSERT INTO weixin_xiaoshuo( title, publishTime, article, publicName, cite) VALUES (%s, %s, %s, %s, %s)
            """
            self.cursor.execute(sql, (title, publishTime, article, publicName, cite))
            self.conn.commit()
        else:
            print "该文章已经存在于数据库中：", title.encode('utf-8')
        return item

    def close_spider(self, spider):
        self.conn.close()
