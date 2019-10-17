#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from utils import views

if __name__ == '__main__':
    while True:
        question = input()
        answer = views.search(question.encode('utf-8'))
        print("Your question is : ", question, "\nAnswer: ", answer)
