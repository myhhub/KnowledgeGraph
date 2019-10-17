#!/usr/bin/env python
# coding=utf-8

"""
Get the table of actor_to_actor and actor_to_genre.
"""
from __future__ import absolute_import
from __future__ import division    
from __future__ import print_function
                    
import sys          
reload(sys)         
sys.setdefaultencoding('utf-8')
                    
import pymysql      
from pymysql import connections
import numpy as np
import re

class connec_mysql(object):
    def __init__(self):    
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            passwd='nlp',
            db='hudong_baike',
            charset='utf8mb4',
            use_unicode=True
            )              
        self.cursor = self.conn.cursor()

    def process_actor_gen(self):
        actor_gen_id = 0
        self.cursor.execute("SELECT MAX(actor_id) FROM actor_back")
        max_actor_id = self.cursor.fetchall()[0][0]
        assert isinstance(max_actor_id, int)
        for actor_id in range(1, max_actor_id + 1):
#        for actor_id in range(1, 1 + 10):
            self.cursor.execute("SELECT * FROM actor_back WHERE actor_id = {};".format(actor_id))
            result = self.cursor.fetchall()
            if np.shape(result) != (1, 11):
                continue
            new_actor_list = [ result[0][i].replace(u'title="" href=""', "") if not isinstance(result[0][i], int) else result[0][i] for i in range(0, 11) ]
            new_actor_list = [ new_actor_list[i].strip(u' 《》') if not isinstance(new_actor_list[i], int) else new_actor_list[i] for i in range(0, 11) ]
            new_actor_tuple = tuple(new_actor_list)
            sql = """ 
                INSERT INTO actor(  actor_id, actor_bio, actor_chName, actor_foreName, actor_nationality, actor_constellation, actor_birthPlace, actor_birthDay, actor_repWorks, actor_achiem, actor_brokerage ) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
            self.cursor.execute(sql, new_actor_tuple)
            self.conn.commit()

if __name__ == '__main__':
    connec = connec_mysql()
    connec.process_actor_gen()
