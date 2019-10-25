#!/usr/bin/env python
# coding=utf-8
import re
import json
import re
from tqdm import tqdm
from clean import Clean

def get_word_list(filename):
    with open(filename, "r",encoding='utf-8') as inf:
        lines = inf.readlines()
#        print "type line: ", type(lines[0].encode("utf-8"))
        lines = [Clean.clean_word(line, clean_level='title') for line in lines]
        return lines


print(Clean.clean_word(u"\"你好   呀#\"$%^&*@!，。、；：‘’】季    候【"))


def main():
    with open("./410_baidu/410_disambi_infobox.csv",'r',encoding='UTF-8') as inf:
        lines = inf.readlines()
        f = open("./410_baidu/410_disambi_infobox_out.csv", "w",encoding='utf-8')
        list_attr = []
        title_list = get_word_list("./410_baidu/410_title.csv")
        err_count = 0
        counts = {}
        for line in tqdm(lines):
            words = line.strip().split(",")
            disambi = Clean.clean_word(words[0], clean_level='disambi')
            infobox = ",".join(words[1:])
            try:
                info_dict = json.loads(json.loads(infobox))
                for attr in info_dict.keys():
                    clean_attr = Clean.clean_word(attr)
                    info_dict[clean_attr] = info_dict.pop(attr)
                    value = info_dict[clean_attr]
                    clean_attr = clean_attr
                    counts[clean_attr] = counts.setdefault(clean_attr, 0) + 1
                    list_attr.append(clean_attr)
                    value_split = re.split(u"[，。、,/]", value.strip())
                    for v in value_split:
                        v = Clean.clean_word(v).strip(u"等").strip(u"收起")
                        title_list.append(v)
                        f.write("\"" + disambi + "\",\"" + clean_attr + "\",\"" + v + "\"" + "\r\n")
            except Exception as e:
                print(e)
                err_count += 1
        title_list = [t.strip(u"\\") for t in title_list]
        title_list = list(set(title_list))
        list_attr = list(set(list_attr))
        sort_counts = sorted(counts.items(),key = lambda x:x[1],reverse = True)
        with open("./sort_counts.txt", "w",encoding='utf-8') as ouf:
            for i in sort_counts:
                ouf.write(str(i) + "\n")
        with open("./all_attr.txt", "w",encoding='utf-8') as ouf:
            for word_counts in sort_counts:
                if  word_counts[1] >= 10:
                    ouf.write(str(word_counts[0]) + "\n")
        with open("./410_baidu/410_title_new.csv", "w",encoding='utf-8') as ouf:
            for i in title_list:
                ouf.write("\"" + i + "\"\r\n")
        with open("./410_baidu/all_attr.txt", "w",encoding='utf-8') as ouf:
            for i in list_attr:
                ouf.write(i + "\n")

        print("err_count: ", err_count)


if __name__ == '__main__':
    main()
