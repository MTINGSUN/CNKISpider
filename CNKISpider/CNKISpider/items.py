# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CnkispiderItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field()
    organizations = scrapy.Field()
    funds = scrapy.Field()
    abstract = scrapy.Field()
    download_num = scrapy.Field()
    reference_num = scrapy.Field()
    journal = scrapy.Field()  
    year = scrapy.Field()   
