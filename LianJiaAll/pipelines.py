# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class LianjiaallPipeline(object):
    def process_item(self, item, spider):
        return item

# 保存数据
class SavePipeline(object):
    def __init__(self):
        self.client = MongoClient()


    def process_item(self, item, spider):
        if item:
            print(item, "================================================")
            province = str(item["province"])
            city = str(item["city"])
            if province and city:
                self.client[province][city].insert_one(item)
                return item
            else:
                return None

# 去重
class UniquePipeline(object):
    def __init__(self):
        self.client = MongoClient()

    def process_item(self, item, spider):
        province = str(item["province"])
        city = str(item["city"])
        if self.client[province][city].find_one(item):
            return None
        else:
            return item

# 清洗
class ClearPipeline(object):
    pass


