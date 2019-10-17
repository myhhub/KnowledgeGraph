#!/usr/bin/env python
# coding=utf-8
from deepdive import *
import re

@tsv_extractor    
@returns(lambda   
        p1_id       = "text",
        p1_name     = "text",
        p2_id           = "text",
        p2_name  = "text",
    :[])  
def extract(      
        p1_id       = "text",
        p1_name     = "text",
        p2_id           = "text",
        p2_name   = "text",
    ): 
    if not(set(p1_name) <= set(p2_name) or set(p2_name) <= set(p1_name)):
        yield [           
            p1_id,        
            p1_name,      
            p2_id,        
            p2_name,      
        ]       
