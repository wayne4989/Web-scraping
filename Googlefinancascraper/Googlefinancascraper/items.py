# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GooglefinancascraperItem(scrapy.Item):
    # define the fields for your item here like:

    Number =scrapy.Field()
    Date =scrapy.Field()
    Open =scrapy.Field()
    High =scrapy.Field()
    Low =scrapy.Field()
    Close =scrapy.Field()
    Volume =scrapy.Field()