# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YelpscraperItem(scrapy.Item):
	
    Name     = scrapy.Field()
    Address  = scrapy.Field()
    Address2 = scrapy.Field()
    City     = scrapy.Field()
    State    = scrapy.Field()
    Zip      = scrapy.Field()
    Phone    = scrapy.Field()
    Website  = scrapy.Field()
    Email    = scrapy.Field()

# name | Address | Address 2 | City | state | Zip | phone | website