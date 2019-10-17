#DROP DATABASE hudong_duplicate;

CREATE DATABASE hudong_fenlei;

USE hudong_fenlei;

CREATE TABLE lemmas( title VARCHAR(100), title_id INT NOT NULL, abstract TEXT, infobox TEXT, subject VARCHAR(500), disambi VARCHAR(100), redirect VARCHAR(100), curLink TEXT, interPic TEXT, interLink TEXT, exterLink TEXT, relateLemma TEXT, all_text TEXT, PRIMARY KEY(title_id));

ALTER TABLE lemmas CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;

ALTER table lemmas ADD INDEX title_index(title);

#ALTER table lemmas ADD INDEX subject_index(subject);

ALTER table lemmas ADD INDEX disambi_index(disambi);
