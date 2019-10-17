#!/bin/bash

curl -XGET 'localhost:9200/demo/baidu_baike/_search?&pretty' -H 'Content-Type:application/json' -d'
{
    "query":{
        "bool":{
            "filter":{
                "term":{"subj":"朱一龙"}
            }
        }
    }      
}
'

