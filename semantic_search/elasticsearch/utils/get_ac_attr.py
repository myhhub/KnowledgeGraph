#!/usr/bin/env python
# coding=utf-8
import ahocorasick
import pickle
from collections import defaultdict


def dump_ac_attr_dict(attr_mapping_file='../data/attr_mapping.txt', out_path='../data/attr_ac.pkl'):
    A = ahocorasick.Automaton()
    f = open(attr_mapping_file,'r',encoding='UTF-8')
    i = 0
    for line in f:
        parts = line.strip().split(" ")
        for p in parts:
            if p != "":
                A.add_word(p, (i, p))
                i += 1
    A.make_automaton()
    pickle.dump(A, open(out_path, 'wb'))


if __name__ == '__main__':
    dump_ac_attr_dict()
