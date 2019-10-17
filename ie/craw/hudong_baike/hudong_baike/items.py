# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HudongBaikeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # Actor
    actor_id = scrapy.Field()
    actor_bio = scrapy.Field()
    actor_chName = scrapy.Field()
    actor_foreName = scrapy.Field()
    actor_nationality = scrapy.Field()
    actor_constellation = scrapy.Field()
    actor_birthPlace = scrapy.Field()
    actor_birthDay = scrapy.Field()
    actor_repWorks = scrapy.Field()
    actor_achiem = scrapy.Field()
    actor_brokerage = scrapy.Field()

    # movie

    movie_id = scrapy.Field()
    movie_bio = scrapy.Field()
    movie_chName = scrapy.Field()
    movie_foreName = scrapy.Field()
    movie_prodTime = scrapy.Field()
    movie_prodCompany = scrapy.Field()
    movie_director = scrapy.Field()
    movie_screenwriter = scrapy.Field()
    movie_genre = scrapy.Field()
    movie_star = scrapy.Field()
    movie_length = scrapy.Field()
    movie_rekeaseTime = scrapy.Field()
    movie_language = scrapy.Field()
    movie_achiem = scrapy.Field()
