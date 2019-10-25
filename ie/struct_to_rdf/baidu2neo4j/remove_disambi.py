#!/usr/bin/env python
# coding=utf-8
import re
from clean import Clean
from tqdm import tqdm

with open("./410_baidu/410_disambi.csv", "r",encoding='utf-8') as inf:
    title_dict = {}
    count = 0
    lines = inf.readlines()
    for line in tqdm(lines):
        words = line.strip().split("\",\"")
        if len(words) != 4:
            count += 1
        clean_disambi = Clean.clean_word(words[0], 'disambi')
        title_dict[clean_disambi] = words[1:]
    print("Error lines: ", count)
    with open("./410_baidu/410_disambi_new.csv", "w",encoding='utf-8') as ouf:
        for i in title_dict.keys():
            ouf.write("\"" + i + "\",\"" + "\",\"".join(title_dict[i]) + "\r\n")
