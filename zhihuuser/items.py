# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    user_type = scrapy.Field()
    badge = scrapy.Field()
    is_following = scrapy.Field()
    url_token = scrapy.Field()
    allow_message = scrapy.Field()
    articles_count = scrapy.Field()
    is_blocking = scrapy.Field()
    is_advertiser = scrapy.Field()
    gender = scrapy.Field()
    headline = scrapy.Field()
    url = scrapy.Field()
    avatar_url = scrapy.Field()
    is_org = scrapy.Field()
    follower_count = scrapy.Field()
    answer_count = scrapy.Field()
    employments = scrapy.Field()



