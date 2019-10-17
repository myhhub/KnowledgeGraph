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

    def select_from_db(self, target_item, target_table, target_condition, target_value):
        self.cursor.execute("SELECT %s FROM %s WHERE %s = %s",
                            (target_item, target_table, target_condition, target_value))
        result = self.cursor.fetchall()
        return result

    def get_json(self):
        for cate in ["actor", "movie"]:
            cate = cate.strip()
            self.cursor.execute("SELECT MAX({}_id) FROM {}".format(cate, cate))
            result = self.cursor.fetchall()
            max_id = result[0][0] if result[0][0] != None else 0
            print("max_id: ", max_id)
            f = open("{}.json".format(cate), "w+")
            for id in range(1, max_id + 1):
                self.cursor.execute("SELECT * FROM {} WHERE {}_id = {}".format(cate, cate, id))
                item_lists = self.cursor.fetchall()
                #                self.cursor.execute("SELECT COLUMN FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{}'".format(cate))
                actor_column_attr = ["actor_id", "actor_bio", "actor_chName", "actor_foreName", "actor_nationality",
                                     "actor_constellation", "actor_birthPlace", "actor_birthDay", "actor_repWorks",
                                     "actor_achiem", "actor_brokerage"]
                movie_column_attr = ["movie_id", "movie_bio", "movie_chName", "movie_foreName", "movie_prodTime",
                                     "movie_prodCompany", "movie_director", "movie_screenwriter", "movie_genre",
                                     "movie_star", "movie_length", "movie_rekeaseTime", "movie_language",
                                     "movie_achiem"]
                column_attr = actor_column_attr if cate == "actor" else movie_column_attr

                if item_lists == None and column_attr == None:
                    continue
                try:
                    assert len(item_lists[0]) == 14 or len(item_lists[0]) == 11
                    item_dict = defaultdict(list)
                    item_dict["subj"] = str(item_lists[0][2])
                    list_po = []
                    for i in range(1, len(item_lists[0])):
                        if column_attr[i] == "{}_chName".format(cate):  # skip actor_chName
                            continue
                        tmp_dict = {}
                        tmp_dict["pred"] = column_attr[i]
                        tmp_dict["obj"] = item_lists[0][i]
                        list_po.append(tmp_dict)
                    item_dict["po"] = list_po
                    item_json = json.dumps(item_dict)
                    f.write(item_json + "\n")

                except Exception as e:
                    print(e)


if __name__ == "__main__":
    connect_sql = connec_mysql()
    connect_sql.get_json()
