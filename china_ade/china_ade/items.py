# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ChinaAdeItem(scrapy.Item):
    title = scrapy.Field()
    dict_data = scrapy.Field()
    item_img = scrapy.Field()
    content = scrapy.Field()
    com_jieshao = scrapy.Field()
    contact_man = scrapy.Field()
    contact_zuoji = scrapy.Field()
    contact_phone = scrapy.Field()
    contact_address = scrapy.Field()
    image_path = scrapy.Field()
    detail_dict = scrapy.Field()
    item_class = scrapy.Field()
    com_file_dict = scrapy.Field()
    com_name = scrapy.Field()

