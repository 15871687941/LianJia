# -*- coding: utf-8 -*-
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
