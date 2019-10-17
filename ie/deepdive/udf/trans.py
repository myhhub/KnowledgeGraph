#!/usr/bin/env python
# coding=utf-8


with open("baidu_baike/articles.txt",encoding='utf-8') as f:
    with open("./articles.csv", "w+",encoding='utf-8') as o:
        lines = f.readlines()
        for line in lines:
            words = line.strip().split(",")
            id = words[0]
            content = words[1:]
            text = '，'.join(content)
            text = text.replace(",", "，")
            o.write(id + "," + text + "\n")

