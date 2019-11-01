#!/usr/bin/env python
# coding=utf-8
# import subprocess
from tqdm import tqdm
import re
import os
from collections import defaultdict
import json
import string
from clean import Clean
import jieba
import pickle
import logging
from stanfordcorenlp import StanfordCoreNLP
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--stanford_path", type=str, default="C:\my\stanford-corenlp")
parser.add_argument("--jieba_dict", type=str, default="data/410_jieba.txt",
                    help="file with all cleaned title to help seg words")
parser.add_argument("--raw_sql_input", type=str, default="data/6w_disambi_text.csv")
parser.add_argument("--raw_sql_output", type=str, default="data/6w_clean_disambi_text.csv")
parser.add_argument("--train_file", type=str, default="data/train.json")
parser.add_argument("--test_file", type=str, default="data/test.json")
parser.add_argument("--disambi_attr_title", type=str, default="data/410_disambi_attr_title.csv",
                    help="csv file include (disambi attribute  title) pair")
parser.add_argument("--title_path", type=str, default="data/410_title.csv")
parser.add_argument("--disambi_title", type=str, default="data/410_title_disambi.csv")
parser.add_argument("--disambi_title_path", type=str, default="data/disambi_title.pkl")
parser.add_argument("--disambi_path", type=str, default="data/disambi_dict.pkl")
parser.add_argument("--max_sentence", type=int, default="1000000")
parser.add_argument("--un_ner_list", type=str, default="[u'O', u'MONEY', u'PERCENT', u'DATE', u'NUMBER', u'ORDINAL']",
                    help="a list include all unused ner tags in StanfordCoreNLP")
parser.add_argument("--max_NA_in_lemmas", type=int, default=15)
parser.add_argument("--max_relation_in_sentence", type=int, default=1)
args = parser.parse_args()


def clean_sql_output(in_file, out_file):
    with open(in_file, "r", encoding='utf-8') as inf, open(out_file, "w", encoding='utf-8') as ouf:
        total_lines = linecount(in_file)
        for line_num in tqdm(range(total_lines)):
            line = inf.readline()
            line = re.sub(u"[\.\!#&%@\^\*\(\)\+“”：』『《》$￥\<\>\\\:\{\}]", "", line)
            line = re.sub(u"\[.*?\]", "", line)
            if not line.endswith("\r\n"):
                ouf.write(line.strip())
            else:
                ouf.write(line.strip() + "\n")


def get_title(infile):
    all_title = set([])
    for line in LoadFile.readline(infile):
        title_tmp = Clean.clean_word(line.strip(), clean_level="title")
        title_tmp = title_tmp.strip().strip("\"")
        if title_tmp == "":
            continue
        all_title.add(title_tmp)
    return all_title


def build_relation_dict(rfile, tfile):
    """
    :rfile relation file
    :tfile title file
    :yield disambi_dict which both title and attr are title
    """
    error_counts = 0
    relation_title = []
    pre_disambi = ""
    all_title = get_title(tfile)
    for line in LoadFile.readline(rfile):
        relation_list = [l.strip("\"") for l in line.split(",")]
        if len(relation_list) != 3:
            error_counts += 1
            continue
        disambi_tmp = relation_list[0]
        relation_tmp = relation_list[1].strip().strip("\"")
        title_tmp = relation_list[2].strip().strip("\"")
        if title_tmp in all_title:
            yield disambi_tmp, relation_tmp, title_tmp
    print("error_counts: ", error_counts)


class DictGenerator(object):
    def __init__(self):
        self.disambi = []
        self.title = []

    def relation_key_tuple(self, rfile, tfile):
        pre_disambi = ""
        relation_title = []
        generator_br = build_relation_dict(rfile, tfile)
        for disambi, relation, title in generator_br:
            if pre_disambi != "" and pre_disambi != disambi:
                if relation_title != []:
                    self.disambi.append(pre_disambi)
                    self.title.append(relation_title)
                    yield pre_disambi, relation_title
                pre_disambi = disambi
                relation_title = []
            elif pre_disambi == "":
                pre_disambi = disambi
            relation_title.append((relation, title))

    def get_disambi_title(self, infile):
        disambi_title = {}
        for line in LoadFile.readline(infile):
            words = line.strip().split("\",\"")
            title_tmp = Clean.clean_word(words[1], clean_level="title")
            disambi_tmp = Clean.clean_word(words[0], clean_level="disambi")
            #            title_tmp = title_tmp.strip().strip("\"")
            disambi_title[disambi_tmp] = title_tmp
        return disambi_title

    def title_title_pair(self, infile):
        """
        func title_title_pair should be run after relation_key_tuple
        """
        if self.disambi == [] or self.title == []:
            raise Exception("func title_title_pair should be run after relation_key_tuple")
        disambi_title = self.get_disambi_title(infile)
        tt_pair = set([])
        for i, attr_tuple in enumerate(self.title):
            cur_disambi = self.disambi[i]
            if cur_disambi in disambi_title:
                cur_title = disambi_title[cur_disambi]
                for rela_attr in attr_tuple:
                    if len(rela_attr) != 2:
                        print("Error in title_title_pair")
                    tt_pair.add(cur_title + "#" + rela_attr[1])
        return tt_pair


class LoadFile(object):
    @staticmethod
    def dump_pkl(oupkl, *args):
        with open(oupkl, "wb") as pf:
            for d in args:
                pickle.dump(d, pf)

    @staticmethod
    def load_pkl(inpkl, data_len):
        with open(inpkl, "rb", encoding='utf-8') as pf:
            data = []
            for i in range(data_len):
                data.append(pickle.load(pf))
        return data

    @staticmethod
    def readline(infile):
        with open(infile, "r", encoding='utf-8') as inf:
            lines_num = linecount(infile)
            for i in range(lines_num):
                yield inf.readline()


def load_dict(rfile, regen=True, disambi_path=args.disambi_path, disambi_title_path=args.disambi_title_path,
              tfile=args.title_path, dt_file=args.disambi_title):
    os.system("mkdir data")
    if regen:
        dg = DictGenerator()
        disambi_dict = {k: v for k, v in dg.relation_key_tuple(rfile, tfile)}
        set_tt_pair = dg.title_title_pair(dt_file)
        LoadFile.dump_pkl(disambi_path, disambi_dict)
        LoadFile.dump_pkl(disambi_title_path, set_tt_pair)
    else:
        disambi_dict = LoadFile.load_pkl(disambi_path, 1)[0]
        set_tt_pair = LoadFile.load_pkl(disambi_title_path, 1)[0]
    return disambi_dict, set_tt_pair


u_list = eval(args.un_ner_list)


def un_ner(ner1):
    # 是 ner 返回 False
    pos1_ner = [i[1] for i in nlp.ner(ner1.encode('utf-8'))]
    if True not in [i not in u_list for i in pos1_ner]:
        return True
    else:
        return False


def build_entity_relation(in_file, train_file, test_file, rfile, tfile=args.title_path):
    with open(in_file, "r", encoding='utf-8') as inf, open(train_file, "w", encoding='utf-8') as trf, open(test_file, "w", encoding='utf-8') as tef:
        disambi_dict, tt_pair_set = load_dict(rfile, regen=True)
        all_title = get_title(tfile)
        title_id = {k: n for n, k in enumerate(all_title)}
        disambi_id = {k: n for n, k in enumerate(disambi_dict.keys())}
        #        print("tt_pair_set: ", tt_pair_set)
        total_lines = linecount(in_file)
        error_counts = 0
        RESID = 0
        RES_list = []
        count_re = 0
        count_na = 0
        total_sentence_used = 0
        re_set = set([])
        # each line here is all_text for lemma
        #        re_in_lemma = 0
        for line_num in tqdm(range(total_lines)):
            re_in_lemma = 0
            if count_na + count_re > args.max_sentence:
                #                re_in_lemma = 0
                continue
            all_info = inf.readline().strip()
            title_disambi_text = all_info.split(",")
            if len(title_disambi_text) != 3:
                error_counts += 1
                continue
            text_title = Clean.clean_word(title_disambi_text[0], clean_level="title")
            text_disambi = Clean.clean_word(title_disambi_text[1], clean_level="disambi")
            all_text = title_disambi_text[2].replace("\"", "")
            try:
                relation_tuple = disambi_dict[text_disambi]
            except:
                continue
            if relation_tuple == "":
                error_counts += 1
                continue
            lines = re.split(u"[。？；！!?]", all_text)
            #            relation_in_sentence = 0
            for r_tuple in relation_tuple:
                if un_ner(text_title) or un_ner(r_tuple[1]):
                    continue
                sentence_used = False
                for line in lines:
                    RES_sentence_dict = {}
                    RES_head_dict = {}
                    RES_tail_dict = {}
                    line = line.strip().replace(" ", "") + u"。"
                    seg_line = " ".join(jieba.cut(line))
                    pos1 = string.find(seg_line, text_title)
                    pos2 = string.find(seg_line, r_tuple[1])
                    if pos1 != -1 and pos2 != -1 and pos1 != pos2:
                        if count_re > args.max_sentence * 0.25:
                            continue
                        if r_tuple[0] != "":
                            count_re += 1
                            re_in_lemma += 1
                            sentence_used = True
                            RES_head_dict['word'] = text_title
                            RES_head_dict['id'] = str(disambi_id[text_disambi])
                            RES_head_dict['type'] = "None"
                            RES_tail_dict['word'] = r_tuple[1]
                            RES_tail_dict['id'] = str(title_id[r_tuple[1]])
                            RES_tail_dict['type'] = "None"
                            RES_sentence_dict['sentence'] = seg_line
                            RES_sentence_dict['head'] = RES_head_dict
                            RES_sentence_dict['tail'] = RES_tail_dict
                            RES_sentence_dict['relation'] = r_tuple[0]
                            RES_list.append(RES_sentence_dict)
                            RESID += 1
                            re_set.add(r_tuple[0])
            for line in lines:
                if count_na > args.max_sentence * 0.75 or re_in_lemma > args.max_NA_in_lemmas:
                    break
                sentence_used = False
                relation_in_sentence = 0
                RES_sentence_dict = {}
                RES_head_dict = {}
                RES_tail_dict = {}
                line = line.strip().replace(" ", "") + u"。"
                seg_line = " ".join(jieba.cut(line))
                words = seg_line.split()
                words = [Clean.clean_word(word, clean_level="others") for word in words]
                enti_pos = []
                for i in range(len(words)):
                    if words[i] != u'' and words[i] in all_title and not un_ner(words[i]):
                        enti_pos.append(i)
                enti_pair_pos = []
                for i in enti_pos:
                    for j in enti_pos:
                        if i != j and not ((words[i] + "#" + words[j]) in tt_pair_set):
                            enti_pair_pos.append((words[i], words[j]))
                if enti_pair_pos == []:
                    continue
                for enti_pair in enti_pair_pos:
                    if relation_in_sentence > args.max_relation_in_sentence or re_in_lemma > args.max_NA_in_lemmas:
                        break
                    count_na += 1
                    relation_in_sentence += 1
                    re_in_lemma += 1
                    sentence_used = True
                    RES_head_dict['word'] = enti_pair[0]
                    RES_head_dict['id'] = str(title_id[enti_pair[0]])
                    RES_head_dict['type'] = "None"
                    RES_tail_dict['word'] = enti_pair[1]
                    RES_tail_dict['id'] = str(title_id[enti_pair[1]])
                    RES_tail_dict['type'] = "None"
                    RES_sentence_dict['sentence'] = seg_line
                    RES_sentence_dict['head'] = RES_head_dict
                    RES_sentence_dict['tail'] = RES_tail_dict
                    RES_sentence_dict['relation'] = "NA"
                    RES_list.append(RES_sentence_dict)
                    RESID += 1
                if sentence_used == True:
                    total_sentence_used += 1
            print("Total Realtion: ", count_re + count_na, "\t Current RE: ", count_re, "\t Current NA: ", count_na)
        with open("rel2id.json", "w") as rf:
            relation_id = {k: v + 1 for v, k in enumerate(re_set)}
            relation_id['NA'] = 0
            rf.write(json.dumps(relation_id))
        print("count_re: ", count_re, "\t count_na: ", count_na, "\t count_total: ", count_re + count_na)
        print("total_sentence_used: ", total_sentence_used)
        total_len = count_re + count_na if count_re + count_na < args.max_sentence else args.max_sentence
        train_list = RES_list[:int(0.8 * total_len)]
        test_list = RES_list[int(0.8 * total_len) + 1:]
        json.dump(train_list, trf)
        json.dump(test_list, tef)


def linecount(file_path):
    count = -1
    for count, line in enumerate(open(file_path, 'r', encoding='utf-8')): pass
    return count + 1


if __name__ == '__main__':
    # use StanfordCoreNLP to tag ner 
    nlp = StanfordCoreNLP(args.stanford_path, lang='zh', logging_level=logging.WARNING)

    # use jieba to seg sentence
    #    jieba.load_userdict(args.jieba_dict)

    clean_sql_output(args.raw_sql_input, args.raw_sql_output)
    build_entity_relation(args.raw_sql_output, args.train_file, args.test_file, args.disambi_attr_title)
