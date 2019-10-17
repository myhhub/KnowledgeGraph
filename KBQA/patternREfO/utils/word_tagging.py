# encoding=utf-8

"""

@author: SimmerChan

@contact: hsl7698590@gmail.com

@file: word_tagging.py

@time: 2017/12/20 15:31

@desc: 定义Word类的结构；定义Tagger类，实现自然语言转为Word对象的方法。

"""
import jieba
import jieba.posseg as pseg


class Word(object):
    def __init__(self, token, pos):
        self.token = token
        self.pos = pos


class Tagger:
    def __init__(self, dict_paths):
        # TODO 加载外部词典
        for p in dict_paths:
            jieba.load_userdict(p)

    def get_word_objects(self, sentence):
        """
        Get :class:WOrd(token, pos)
        """
        return [Word(bytes.decode(word.encode('utf-8')), tag) for word, tag in pseg.cut(sentence)]

if __name__ == '__main__':
    tagger = Tagger(['../data/actorName.txt', '../data/movieName.txt'])
    while True:
        s = input()
        print("tagger.get_word_objects(s): ", tagger.get_word_objects(s))
        for i in tagger.get_word_objects(s):
            print(i.token, i.pos)
