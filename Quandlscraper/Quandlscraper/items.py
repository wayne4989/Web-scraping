# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QuandlscraperItem(scrapy.Item):

    Date = scrapy.Field()
    ID  = scrapy.Field()
    Data = scrapy.Field()


class QuandlurlItem(scrapy.Item):

    url = scrapy.Field()
    ID = scrapy.Field()

        