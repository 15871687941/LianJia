# -*- coding: utf-8 -*-
import scrapy
from LianJiaAll.items import LianjiaallItem
import math
import uuid
import copy


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://www.lianjia.com/city/']

    def parse(self, response):
        item = LianjiaallItem()
        # 找到所有包含省市的元素
        province_eles = response.css("div.city_province")
        for province_ele in province_eles:
            province = province_ele.xpath("./div[@class='city_list_tit c_b']/text()").get()
            # print(province, "=============================================================")
            city_eles = province_ele.xpath("./ul/li/a")
            for city_ele in city_eles:
                city = city_ele.xpath("./text()").get()
                url = city_ele.xpath("./@href").get()
                if "fang" in url:
                    continue
                item["province"] = province
                item["city"] = city
                # 如果没有深拷贝，就会导致所有的item都会公用一片内存
                item = copy.deepcopy(item)
                yield scrapy.Request(url=url, callback=self.parse_city, meta={"item": item})


    def parse_city(self, response):
        item = response.meta["item"]
        print(item, "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
        url = response.url + "ershoufang/"
        return scrapy.Request(url=url, callback=self.parse_block, meta={"item": item})

    def parse_block(self, response):
        item = response.meta["item"]
        block_eles = response.xpath("//div[@class='position']/dl[2]/dd/div/div[1]")
        for block_ele in block_eles:
            block = block_ele.xpath("./a/text()").get()
            print(block)
            print(response.url[0:-12], "==========================================")
            print(block_ele.xpath("./a/@href").get(), "=======================================")
            url = response.url[0:-12] + block_ele.xpath("./a/@href").get()
            print(url, "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            item["block"] = block
            yield scrapy.Request(url=url, callback=self.parse_block_page, meta={"item": item, "selenium": True})

    def parse_block_page(self, response):
        item = response.meta["item"]
        print(item, "===============================================")
        count = int(response.xpath("//h2[@class='total fl']/span/text()").get().strip())
        if math.ceil(int(count) / 30) > 100:
            max_page = 100
        else:
            max_page = math.ceil(int(count) / 30)
        base_url = response.url + "pg%dco32/"
        for page in range(1, max_page + 1):
            url = base_url % page
            yield scrapy.Request(url=url, callback=self.parse_block_item, meta={"item": item})

    def parse_block_item(self, response):
        item = response.meta["item"]
        item_urls = response.xpath("//div[@class='info clear']/div[@class='title']/a/@href").getall()
        for item_url in item_urls:
            url = item_url
            yield scrapy.Request(url=url, callback=self.parse_item_detail, meta={"item": item})

    def parse_item_detail(self, response):
        item = response.meta["item"]
        item["_id"] = uuid.uuid1().hex
        item["loc"] = ",".join(response.xpath("//div[@class='areaName']/span[@class='info']/a/text()").getall())
        item["room"] = ",".join(response.xpath("//div[@class='room']/div/text()").getall())
        item["type"] = ",".join(response.xpath("//div[@class='type']/div/text()").getall())
        item["area"] = ",".join(response.xpath("//div[@class='area']/div/text()").getall())
        item["price"] = response.xpath("//div[@class='price ']/span[@class='total']/text()").get() + "万"
        item["unitPrice"] = response.xpath("//span[@class='unitPriceValue']/text()").get() + "元/平米"
        item["url"] = response.url
        return item






