# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Post(scrapy.Item):
    post_id = scrapy.Field()
    creator_id = scrapy.Field()
    language = scrapy.Field()
    first_published_at = scrapy.Field()
