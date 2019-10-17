#!/usr/bin/env python
# coding=utf-8

from deepdive import *        
import random                 
from collections import namedtuple
                              
PlayLabel = namedtuple('PlayLabel', 'p1_id, p2_id, label, type')
                              
@tsv_extractor                
@returns(lambda               
        p1_id   = "text",     
        p2_id   = "text",     
        label   = "int",      
        rule_id = "text",     
    :[])                      
# heuristic rules for finding positive/negative examples of play relationship mentions
def supervise(                
        p1_id="text", p1_begin="int", p1_end="int",
        p2_id="text", p2_begin="int", p2_end="int",
        doc_id="text", sentence_index="int", sentence_text="text",
        tokens="text[]", lemmas="text[]", pos_tags="text[]", ner_tags="text[]",
        dep_types="text[]", dep_token_indexes="int[]",
    ):
    PLAY = frozenset(["出演", "主演", "参演", "友情出演", "饰演", "特别出演"])

    COMMAS = frozenset([":", "：","1","2","3","4","5","6","7","8","9","0","、", ";", "；"])
    MAX_DIST = 40

    # Common data objects
    intermediate_lemmas = lemmas[p1_end+1:p2_begin]
    intermediate_ner_tags = ner_tags[p1_end+1:p2_begin]
    tail_lemmas = lemmas[p2_end+1:]
    play = PlayLabel(p1_id=p1_id, p2_id=p2_id, label=None, type=None)

    if len(intermediate_lemmas) > MAX_DIST:
        yield play._replace(label=-1, type='neg:far_apart')
    
    if 'PERSON' in intermediate_ner_tags:
        yield play._replace(label=-1, type='neg:third_person_between')

    if len(COMMAS.intersection(intermediate_lemmas)) > 0:
        yield play._replace(label=-1, type='neg:中间有特殊符号')

    if len(PLAY.intersection(intermediate_lemmas)) > 0:
        yield play._replace(label=1, type='pos:A出演B')
