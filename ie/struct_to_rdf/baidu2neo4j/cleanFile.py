#!/usr/bin/env python
# coding=utf-8
from tqdm import tqdm
from clean import Clean
def clean_title_disambi(infile="title_disambi.csv", outfile="title_disambi_out.csv"):
    with open(infile, "r",encoding='utf-8') as inf:
        lines = inf.readlines()
        err_counts = 0
        with open(outfile, "w",encoding='utf-8') as ouf:
            for line in tqdm(lines):
                words = line.strip().split("\",\"")
                if len(words) != 2:
                    err_counts += 1
                    continue
                title = Clean.clean_word(words[0], clean_level='title')
                disambi = Clean.clean_word(words[1], clean_level='disambi')
                ouf.write("\"" + title + "\",\"" + disambi + "\"\r\n")
            print("err_counts for disambi_redirect: ", err_counts)


def clean_disambi_redirect(infile="disambi_redirect.csv", outfile="disambi_redirect_out.csv"):
    with open(infile, "r",encoding='utf-8') as inf:
        lines = inf.readlines()
        err_counts = 0
        with open(outfile, "w",encoding='utf-8') as ouf:
            for line in tqdm(lines):
                words = line.strip().split("\",\"")
                if len(words) != 2:
                    err_counts += 1
                    continue
                disambi = Clean.clean_word(words[0], clean_level='disambi')
                redirect = Clean.clean_word(words[1], clean_level='redirect')
                ouf.write("\"" + disambi + "\",\"" + redirect + "\"\r\n")
            print("err_counts for disambi_redirect: ", err_counts)


def clean_disambi_subject(infile="disambi_subject.csv", outfile="disambi_subject_out.csv"):
    with open(infile, "r",encoding='utf-8') as inf:
        lines = inf.readlines()
        err_counts = 0
        with open(outfile, "w",encoding='utf-8') as ouf:
            for line in tqdm(lines):
                words = line.strip().split("\",\"")
                if len(words) != 2:
                    err_counts += 1
                    continue
                disambi = Clean.clean_word(words[0], clean_level='disambi')
                subject = Clean.clean_word(words[1], clean_level='subject')
                ouf.write("\"" + disambi + "\",\"" + subject + "\"\r\n")
            print("err_counts for disambi_redirect: ", err_counts)


if __name__ == '__main__':
    clean_title_disambi(infile="./410_baidu/410_title_disambi.csv", outfile="./410_baidu/410_title_disambi_out.csv")
    clean_disambi_redirect(infile="./410_baidu/410_disambi_redirect.csv", outfile="./410_baidu/410_disambi_redirect_out.csv")
