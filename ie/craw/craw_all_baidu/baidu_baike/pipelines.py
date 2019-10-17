# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from __future__ import absolute_import
from __future__ import division     
from __future__ import print_function

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pymysql
from pymysql import connections
from baidu_baike import settings

class BaiduBaikePipeline(object):
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
        # process info for actor
        title = str(item['title']).decode('utf-8')
        title_id = str(item['title_id']).decode('utf-8')
        abstract = str(item['abstract']).decode('utf-8')
        infobox = str(item['infobox']).decode('utf-8')
        subject = str(item['subject']).decode('utf-8')
        disambi = str(item['disambi']).decode('utf-8')
        redirect = str(item['redirect']).decode('utf-8')
        curLink = str(item['curLink']).decode('utf-8')
        interPic = str(item['interPic']).decode('utf-8')
        interLink = str(item['interLink']).decode('utf-8')
        exterLink = str(item['exterLink']).decode('utf-8')
        relateLemma = str(item['relateLemma']).decode('utf-8')
        all_text = str(item['all_text']).decode('utf-8').encode('utf-8')

#        self.cursor.execute("SELECT disambi FROM lemmas;")
#        disambi_list = self.cursor.fetchall()
#        if (disambi,) not in disambi_list :
        self.cursor.execute("SELECT MAX(title_id) FROM lemmas")
        result = self.cursor.fetchall()[0]
        if None in result:
            title_id = 1
        else:
            title_id = result[0] + 1
        sql = """
        INSERT INTO lemmas(title, title_id, abstract, infobox, subject, disambi, redirect, curLink, interPic, interLink, exterLink, relateLemma, all_text ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
#            disambi_list = self.cursor.fetchall()
#            if (disambi, ) in disambi_list:
#                print ("result: ", disambi)
            self.cursor.execute(sql, (title, title_id, abstract, infobox, subject, disambi, redirect, curLink, interPic, interLink, exterLink, relateLemma, all_text ))
            self.conn.commit()
#            self.cursor.execute("SELECT disambi FROM lemmas" )
        except Exception as e:
            print("#"*20, "\nAn error when insert into mysql!!\n")
            print("curLink: ", curLink, "\n")
            print(e, "\n", "#"*20)
            try:
                all_text = str('None').decode('utf-8').encode('utf-8')
                self.cursor.execute(sql, (title, title_id, abstract, infobox, subject, disambi, redirect, curLink, interPic, interLink, exterLink, relateLemma, all_text ))
                self.conn.commit()
            except Exception as f:
                print("Error without all_text!!!")
        return item

    def close_spider(self, spider):
        self.conn.close()
