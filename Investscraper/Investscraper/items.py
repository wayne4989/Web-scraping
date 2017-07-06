# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InvestscraperItem(scrapy.Item):
    # define the fields for your item here like:
    Curr_Id      = scrapy.Field()
    Date         = scrapy.Field()
    Price        = scrapy.Field()
    Open         = scrapy.Field()
    High         = scrapy.Field()
    Low          = scrapy.Field()
    Vol          = scrapy.Field()
