# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DataItem(scrapy.Item):
    # define the fields for your item here like:
    date = scrapy.Field()
    value = scrapy.Field()
    chartID = scrapy.Field()
    
class ChartItem(scrapy.Item):
    # define the fields for your item here like:
    VariableID = scrapy.Field()
    ChartID = scrapy.Field()
    Chartname = scrapy.Field()
    pass