# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PradascraperItem(scrapy.Item):
	
    City      = scrapy.Field()
    Name      = scrapy.Field()
    Address   = scrapy.Field()
    Latitute  = scrapy.Field()
    Longitude = scrapy.Field()
    Shoptype  = scrapy.Field()
    Brand     = scrapy.Field()
    Date      = scrapy.Field()