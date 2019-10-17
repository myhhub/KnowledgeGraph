#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    import simplejson as json
except:
    import json

import pymysql
from pymysql import connections
from collections import defaultdict


class connec_mysql(object):
    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            passwd='root',
            db='baidu_baike',
            charset='utf8mb4',
            use_unicode=True
        )
        self.cursor = self.conn.cursor()

    def get_actor_movie(self, filename, out_name):
        outfile = open(out_name,'w',encoding='UTF-8')
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                words = line.strip().split()
                if len(words) != 2:
                    print("Got line with wrong fromat~")
                    continue
                actor_id = words[0]
                movie_id = words[1]
                self.cursor.execute(
                    "SELECT actor_chName, actor_foreName FROM actor WHERE actor_id = {}".format(actor_id))
                actor_list = self.cursor.fetchall()
                actor_chName, actor_foreName = actor_list[0]
                self.cursor.execute(
                    "SELECT movie_chName, movie_foreName FROM movie WHERE movie_id = {}".format(movie_id))
                movie_list = self.cursor.fetchall()
                movie_chName, movie_foreName = movie_list[0]
                for item_actor in [actor_chName, actor_foreName]:
                    for item_movie in [movie_chName, movie_foreName]:
                        if item_actor not in ["None", ""] and item_movie not in ["None", ""]:
                            outfile.write(item_actor + "," + item_movie + "\n")

        outfile.close()


if __name__ == "__main__":
    connect_sql = connec_mysql()
    connect_sql.get_actor_movie("../input/actor_movie.txt", "../input/actor_movie_dbdata.csv")
