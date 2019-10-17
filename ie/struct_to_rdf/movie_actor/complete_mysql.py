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

    def process_act_movie(self):
        actor_movie_id = 0
        self.cursor.execute("SELECT MAX(actor_id) FROM actor")
        max_actor_id = self.cursor.fetchall()[0][0]
        assert isinstance(max_actor_id, int)
        for actor_id in range(1, max_actor_id + 1):
            self.cursor.execute("SELECT actor_repworks FROM actor WHERE actor_id = {};".format(actor_id))
            result = self.cursor.fetchall()
            assert np.shape(result) == (1, 1) # if didn't exist, return (0, )
            repworks = re.split(u"[，/、 ]", result[0][0] )
            try:
                assert len(repworks) > 0
                for repwork in repworks:
                    repwork = repwork.strip(u" 《》")
                    self.cursor.execute("SELECT movie_id FROM movie WHERE movie_chName = %s", repwork)
                    check_movie_id = self.cursor.fetchall()
                    if len(check_movie_id) != 0:
                        self.cursor.execute("INSERT INTO actor_to_movie (actor_movie_id, actor_id, movie_id) VALUES (%s, %s, %s)", (actor_movie_id, actor_id, check_movie_id[0][0]) )
                        self.conn.commit()
                        actor_movie_id += 1
            except Exception as e:
                print("Get a error with ", e, "Maybe this actor has no represent works")
                continue

    def process_movie_gen(self):
        movie_gen_id = 0
        self.cursor.execute("SELECT MAX(movie_id) FROM movie")
        max_movie_id = self.cursor.fetchall()[0][0]
        assert isinstance(max_movie_id, int)
        for movie_id in range(1, max_movie_id + 1):
#        for movie_id in range(1, 1 + 10):
            self.cursor.execute("SELECT movie_genre FROM movie WHERE movie_id = {};".format(movie_id))
            result = self.cursor.fetchall()
            if np.shape(result) != (1, 1):
                continue
            movie_genres = re.split(u"[，/、 ]", result[0][0] )
#            print("movie_genres: ", movie_genres)
            try:
                assert len(movie_genres) > 0
                for movie_genre in movie_genres:
                    self.cursor.execute("SELECT genre_id FROM genre WHERE genre_name = %s", movie_genre)
                    check_genre_id = self.cursor.fetchall()
                    if len(check_genre_id) != 0:
                        self.cursor.execute("INSERT INTO movie_to_genre (movie_genre_id, movie_id, genre_id) VALUES (%s, %s, %s)", (movie_gen_id, movie_id, check_genre_id[0][0]) )
                        self.conn.commit()
                        movie_gen_id += 1
            except Exception as e:
                print("Get a error with ", e)
                continue
if __name__ == '__main__':
    connec = connec_mysql()
#    connec.process_act_movie()
    connec.process_movie_gen()
