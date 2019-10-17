#!/usr/bin/env python
# coding=utf-8

from collections import defaultdict
from clean import Clean
from tqdm import tqdm

with open("./410_baidu/410_disambi_subject.csv") as inf:
    lines = inf.readlines()
#    all_subject = defaultdict(list)
    total_subject = []
    f = open("./410_baidu/disambi_subject.csv", "w")
    for line in tqdm(lines):
        words = line.strip().split(",")
        disambi = Clean.clean_word(words[0].decode('utf-8'), clean_level='disambi').encode("utf-8")
        subjects = words[1:]
        subjects = [Clean.clean_word(s.decode('utf-8'), clean_level="subject").encode("utf-8") for s in subjects]
#        subjects = [s.replace("\"", "").strip("\\") for s in subjects]
#        subjects = [s.strip() for s in subjects]
        total_subject.extend(subjects)
        for subject in subjects:
            if subject == "":
                continue
            f.write("\"" + disambi + "\",\"" + subject + "\"\r\n")
#        all_subject[disambi].append(subjects)
    f.close()
    total_subject = list(set(total_subject))
    print "Total subjects: ", len(total_subject)
    with open("./410_baidu/all_subject.csv", "w") as ouf:
        ouf.write("\"" + "\"\n\"".join(total_subject) + "\"")
