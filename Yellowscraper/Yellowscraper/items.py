# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YellowscraperItem(scrapy.Item):

    Title            		= scrapy.Field()
    Address		= scrapy.Field()
    Phone          = scrapy.Field()
    Distance           = scrapy.Field()
    Category           = scrapy.Field()
    # product_NumberOfReviews = scrapy.Field()