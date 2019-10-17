#!/bin/bash

# Export dict for movie and actor in hudong and baidu DB;
# You need change the user and pwd for your own DB;
mysql -uroot -pnlp < ./data/get_dict.txt 

sudo cp /var/lib/mysql-files/*Name.txt .

cat baidu_actorName.txt hudong_actorName.txt | sort -u > actorTmp.txt
cat baidu_movieName.txt hudong_movieName.txt | sort -u > movieTmp.txt
# Append "nz" and "nr" tag for jieba
awk '{print $0 " nr"}' actorTmp.txt > actorName.txt
awk '{print $0 " nz"}' movieTmp.txt > movieName.txt

# Remove redundant file
rm ^[am].*Name.txt
