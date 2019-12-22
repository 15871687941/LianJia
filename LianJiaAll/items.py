# -*- coding: utf-8 -*-

# Define here the models for your scraped items
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaallItem(scrapy.Item):
    _id = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    block = scrapy.Field()
    loc = scrapy.Field()
    room = scrapy.Field()
    type = scrapy.Field()
    area = scrapy.Field()
    price = scrapy.Field()
    unitPrice = scrapy.Field()
    url = scrapy.Field()
