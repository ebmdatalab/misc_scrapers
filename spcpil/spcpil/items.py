# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpcpilItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    doc_type = scrapy.Field()  # PIL or SPC
    product = scrapy.Field()
    file_name = scrapy.Field()
    file_urls = scrapy.Field()
