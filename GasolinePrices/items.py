# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GasolinePricesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    price = scrapy.Field()
    gasType = scrapy.Field()
    timestamp = scrapy.Field()