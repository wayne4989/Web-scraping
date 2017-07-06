# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SkinscriptrxscraperItem(scrapy.Item):

    Name     = scrapy.Field()
    Address1 = scrapy.Field()
    Address2 = scrapy.Field()
    City     = scrapy.Field()
    State    = scrapy.Field()
    Zip      = scrapy.Field()
    Phone    = scrapy.Field()
    Email    = scrapy.Field()
    Website  = scrapy.Field()
    Lat      = scrapy.Field()
    Lng      = scrapy.Field()