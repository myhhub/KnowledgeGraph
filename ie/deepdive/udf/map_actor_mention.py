#!/usr/bin/env python
# coding=utf-8

from deepdive import *
import re

@tsv_extractor
@returns(lambda
         mention_id     = "text",
         mention_text   = "text",
         doc_id         = "text",
         sentence_index = "int",
         begin_index    = "int",
         end_index      = "int",
         :[])
def extract(
        doc_id          = "text",
        sentence_index  = "int",
        tokens          = "text[]",
        pos_tags        = "text[]",
        ner_tags        = "text[]",
    ):
    """
    Finds phrases thar are continuous words with POS tags == MISC and NER tags == NN.
    We make this decision due to stanford parser got bad performance when recognizing actor.
    """
    num_tokens = len(ner_tags)
    first_index = ( i for i in xrange(num_tokens) if ner_tags[i] == "PERSON" and pos_tags[i] == "NR" and (i == 0 or (ner_tags[i-1] != "PERSON" and pos_tags[i-1] != "NR" )) and re.match(u'^[\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ffa-zA-Z]+$', unicode(tokens[i], "utf-8")) != None)
    for begin_index in first_index:
        end_index = begin_index + 1
        while end_index < num_tokens and ner_tags[end_index] == "PERSON" and pos_tags[end_index] == "NR" and re.match(u'^[\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ffa-zA-Z]+$', unicode(tokens[end_index], "utf-8")) != None:
            end_index += 1
        end_index -= 1
        mention_id = "%s_%d_%d_%d" % (doc_id, sentence_index, begin_index, end_index)
        mention_text = "".join(map(lambda i: tokens[i], xrange(begin_index, end_index + 1)))

        yield [
            mention_id,
            mention_text,
            doc_id,
            sentence_index,
            begin_index,
            end_index,
        ]

