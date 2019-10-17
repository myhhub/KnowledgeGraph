#!/usr/bin/env python
# coding=utf-8

import re
from refo import finditer, Predicate, Star, Any

# SPARQL config  
SPARQL_PREAMBLE = u"""  
PREFIX : <http://www.kgdemo.com#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""              
                 
SPARQL_TEM = u"{preamble}\n" + \
             u"SELECT DISTINCT {select} WHERE {{\n" + \
             u"{expression}\n" + \
             u"}}\n"    
                 
INDENT = "    "  

class W(Predicate):
    """object-oriented regex for words"""
    def __init__(self, token=".*", pos=".*"):
        self.token = re.compile(token + "$")
        self.pos = re.compile(pos + "$")
        super(W, self).__init__(self.match)
                   
    def match(self, word):
        m1 = self.token.match(word.token)
        m2 = self.pos.match(word.pos)
        return m1 and m2

class Rule(object):
    def __init__(self, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action
            
    def apply(self, sentence):
        matches = []
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            matches.extend(sentence[i:j])
        if __name__ == '__main__':
            pass
        return self.action(matches)

def who_is_question(x):
    select = u"?x0"
            
    sparql = None
    for w in x:
        if w.pos == "nr" or w.pos == "x":
            e = u" ?a :actor_chName '{person}'. \n \
            ?a :actor_bio ?x0".format(person=w.token)
         
            sparql = SPARQL_TEM.format(preamble=SPARQL_PREAMBLE,
                                       select=select,
                                       expression=INDENT + e)
            break   
    return sparql 

def where_is_from_question(x):
    select = u"?x0"
 
    sparql = None 
    for w in x:   
        if w.pos == "nr" or w.pos == "x" or w.pos == "nrt":
            e = u" ?a :actor_chName '{person}'.\n \
            ?a :actor_birthPlace ?x0".format(person=w.token)
 
            sparql = SPARQL_TEM.format(preamble=SPARQL_PREAMBLE,
                                       select=select,
                                       expression=INDENT + e)
            break
    return sparql
 
 
def movie_intro_question(x):
    select = u"?x0"
 
    sparql = None
    for w in x:
        if w.pos == "nz":
            e = u" ?a :movie_chName '{person}'. \n \
            ?a :movie_bio ?x0".format(person=w.token)

            sparql = SPARQL_TEM.format(preamble=SPARQL_PREAMBLE,
                                       select=select,
                                       expression=INDENT + e)
            break
    return sparql

def customize_rules():
    # some rules for matching
    # TODO: customize your own rules here
    person = (W(pos="nr") | W(pos="x") | W(pos="nrt") | W(pos="nz"))
    movie = (W(pos="nz"))
    place = (W("出生地") | W("出生"))
    intro = (W("简介") | W(pos="介绍"))
                                
    rules = [                   
                                
        Rule(condition=W(pos="r") + W("是") + person | \
                       person + W("是") + W(pos="r"),
             action=who_is_question),
                          
        Rule(condition=person + Star(Any(), greedy=False) + place + Star(Any(), greedy=False),
             action=where_is_from_question),
                          
        Rule(condition=movie + Star(Any(), greedy=False) + intro + Star(Any(), greedy=False) ,
             action=movie_intro_question)
                          
    ]
    return rules
