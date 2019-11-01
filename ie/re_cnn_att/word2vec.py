#!/usr/bin/env python
# coding=utf-8
from gensim.models import word2vec
from tqdm import tqdm
import json
import os
import jieba
from gen_re_from_baidu import LoadFile


def cut_words(line):
    seg_line = " ".join(jieba.cut(line))
    return seg_line


def seg_file(infile="", outfile=""):
    with open(outfile, "w", encoding='utf-8') as ouf:
        for line in tqdm(LoadFile.readline(infile)):
            seg_line = cut_words(line)
            ouf.write(seg_line)


def transfer_json(in_file_path, out_file_path):
    with open(in_file_path, "r", encoding='utf-8') as inf:
        ouf = open(out_file_path, "w", encoding='utf-8')
        word_embed_list = []
        word_num, dim = inf.readline().strip().split()
        print("Total word_num: ", word_num, "\nWord dim: ", dim)
        for line_num in tqdm(range(int(word_num))):
            word_dict = {}
            words = inf.readline().strip().split()
            word_dict["word"] = words[0]
            word_dict["vec"] = eval("[" + ",".join(words[1:]) + "]")
            word_embed_list.append(word_dict)
        json.dump(word_embed_list, ouf)


if __name__ == "__main__":
    seg_file(infile="data/6w_clean_disambi_text.csv", outfile="seg_6w_disambi_text.txt")
    os.system("C:\my\word2vec\word2vec  -train seg_6w_disambi_text.txt -output word_vec.txt -size 50 -window 5 -sample 1e-4 -negative 5 -hs 0 -binary 0 -cbow 0 -iter 3 -min-count 1 -hs 1")
    transfer_json("word_vec.txt", "word_vec.json")

