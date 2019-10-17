#!/usr/bin/env python
# coding=utf-8

"""
Get the table of actor_to_movie and movie_to_genre.
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

    def process_movie_gen(self):
        movie_gen_id = 0
        self.cursor.execute("SELECT MAX(movie_id) FROM movie_back")
        max_movie_id = self.cursor.fetchall()[0][0]
        assert isinstance(max_movie_id, int)
        for movie_id in range(1, max_movie_id + 1):
#        for movie_id in range(1, 1 + 1):
            self.cursor.execute("SELECT * FROM movie_back WHERE movie_id = {};".format(movie_id))
            result = self.cursor.fetchall()
            print("np.shape(result): ", np.shape(result))
            if np.shape(result) != (1, 14):
                continue
            new_movie_list = [ result[0][i].strip(u" 《》") if not isinstance(result[0][i], int) else result[0][i] for i in range(0, 14) ]
#            new_movie_list = [result[0][i] if i != 2 else movie_name for i in range(0, 14)]
            new_movie_tuple = tuple(new_movie_list)
            sql = """ 
                INSERT INTO movie(  movie_id, movie_bio, movie_chName, movie_foreName, movie_prodTime, movie_prodCompany,       movie_director, movie_screenwriter, movie_genre, movie_star, movie_length, movie_rekeaseTime, movie_language, movie_achiem )    VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
            self.cursor.execute(sql, new_movie_tuple)
            self.conn.commit()

if __name__ == '__main__':
    connec = connec_mysql()
    connec.process_movie_gen()
