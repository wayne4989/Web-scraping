# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
# Name of Church | Address | City | State | Zip | Phone | Pasors | email | Web | ONA | Accessible
import scrapy


class UccscraperItem(scrapy.Item):

    Name_of_Church = scrapy.Field()
    Address        = scrapy.Field()
    City           = scrapy.Field()
    Fax            = scrapy.Field()
    Latitude       = scrapy.Field()
    Logitude       = scrapy.Field()
    Distance       = scrapy.Field()
    State          = scrapy.Field()
    Zip            = scrapy.Field()
    Phone          = scrapy.Field()
    Pasors         = scrapy.Field()
    Email          = scrapy.Field()
    Web            = scrapy.Field()
    ONA            = scrapy.Field()
    Accessible     = scrapy.Field()