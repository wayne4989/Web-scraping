# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StreetscraperItem(scrapy.Item):

    URL         = scrapy.Field()
    Address     = scrapy.Field()
    Price       = scrapy.Field()
    Abailibity  = scrapy.Field()
    Rooms       = scrapy.Field()
    Beds        = scrapy.Field()
    Baths       = scrapy.Field()
    Sqft        = scrapy.Field()
    Description = scrapy.Field()
    Amenities   = scrapy.Field()
    Location    = scrapy.Field()
    Picture     = scrapy.Field()
    NO_FEE      = scrapy.Field()

class RentscraperItem(scrapy.Item):

    URL         = scrapy.Field()
    Address     = scrapy.Field()
    Price       = scrapy.Field()
    Abailibity  = scrapy.Field()
    Rooms       = scrapy.Field()
    Beds        = scrapy.Field()
    Baths       = scrapy.Field()
    Sqft        = scrapy.Field()
    Description = scrapy.Field()
    Amenities   = scrapy.Field()
    Location    = scrapy.Field()
    Picture     = scrapy.Field()
    NO_FEE      = scrapy.Field()