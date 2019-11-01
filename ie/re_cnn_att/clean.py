#!/usr/bin/env python
# coding=utf-8
import re
import commands


class Clean(object):
    @staticmethod
    def clean_word(word, clean_level='others'):
        """
        Remove symbols in words
        :word word with unicode
        :clean_level keep different symbols for disambi/title
        :return clean word
        """
        word = word.strip()

        if clean_level == "title":
            word = word.strip().strip("\"").replace("\n", " ").replace("\"", "").strip(u"\\")
        elif clean_level == "subject":
            word = word.replace("\"", "").strip("\\").strip()
        elif clean_level == "redirect":
            word = word.strip("\"")
        elif clean_level == "disambi":
            word = re.sub(
                u"[，。、＆∈＊．↑【２—‘：“＃＞ ＢＦＲ·Ｚ<ｂｆ≈ｊ×～①Ⅲ⑤⑨÷〔！％》－』１→５＝ＡＥ∧Ｉ/″▲;］ξａｅφｉ｝④⑧…─☆《『０В＜Ｄ∪Ｌ±γ′ＴＸλ:ｄｈ｜③⑦~、℃＇〉＋」／】３〕Δ’；”？■ＣＧΨ［=μ＿ｃｇβ㈧ｏ｛②⑥'⑩。\~\!\@\#\$\%\^\&\*\(\)\_\-\+\=\{\}\[\]\\\|\:\;\'\"\.\>\?\/\, \xa0\u00a0\u3000]",
                "", word)
        elif clean_level == 'others':
            word = re.sub(
                u"[，。、＆∈＊．↑【２—‘：“＃＞ ＢＦＲ·Ｚ<ｂｆ≈ｊ×～①Ⅲ⑤⑨÷〔！％）》－』１→５＝ＡＥ∧Ｉ/″▲;］ξａｅφｉ｝④⑧…─☆（《『０В＜Ｄ∪Ｌ±γ′ＴＸλ:ｄｈ｜③⑦~、℃＇〉＋」／】３〕Δ’；”？■ＣＧΨ［=μ＿ｃｇβ㈧ｏ｛②⑥'⑩。\~\!\@\#\$\%\^\&\*\(\)\_\-\+\=\{\}\[\]\\\|\:\;\'\"\.\>\?\/\,\xa0\u00a0\u3000\r\n]",
                "", word)
        return word


class ProcessFile(object):
    @staticmethod
    def get_line(self, filename):
        total_lines = commands.getoutput("sed -n '$=' {}".format(filename))
        with open(filename, "r", encoding='utf-8') as inf:
            for line_num in range(total_lines):
                line = inf.readline().strip()
                yield line
