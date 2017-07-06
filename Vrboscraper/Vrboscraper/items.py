# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class VrboscraperItem(scrapy.Item):
    Location = scrapy.Field()
    ID          = scrapy.Field()
    Rate_Night = scrapy.Field()
    Property = scrapy.Field()
    Sleeps = scrapy.Field()
    Bedrooms = scrapy.Field()
    Bathrooms = scrapy.Field()
    Minimum_Stay = scrapy.Field()
    Owner = scrapy.Field()
    Property_Manager = scrapy.Field()
    Link = scrapy.Field()
    Description = scrapy.Field()
