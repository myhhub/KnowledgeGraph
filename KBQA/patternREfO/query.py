#!/usr/bin/env python
# coding=utf-8

from SPARQLWrapper import SPARQLWrapper, JSON
from utils.word_tagging import Tagger
from utils.rules import customize_rules

if __name__ == "__main__":
    print("init...........")
    sparql_base = SPARQLWrapper("http://localhost:3030/kg_movie/query")
    tagger = Tagger(['data/actorName.txt', 'data/movieName.txt'])
    rules = customize_rules()
    print("done \n")

    while True:
        print("Please input your question: ")
        default_question = input()
        seg_list = tagger.get_word_objects(default_question)

        for rule in rules:
            query = rule.apply(seg_list)
            if query:
                sparql_base.setQuery(query)
                sparql_base.setReturnFormat(JSON)
                results = sparql_base.query().convert()
    
                if not results["results"]["bindings"]:
                    print("No answer found :(")
                    continue
                for result in results["results"]["bindings"]:
                    print("Result: ", result["x0"]["value"])
