# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class StayzscraperItem(scrapy.Item):

	Title       = scrapy.Field()
	URL         = scrapy.Field()
	Price       = scrapy.Field()
	Rated       = scrapy.Field()
	Bathrooms   = scrapy.Field()
	Bedrooms    = scrapy.Field()
	Beds        = scrapy.Field()
	Guests      = scrapy.Field()
	Description = scrapy.Field()
	Features    = scrapy.Field()
	Location    = scrapy.Field()
	Picture     = scrapy.Field()
	Reviews     = scrapy.Field()
	Latitude    = scrapy.Field()
	Longitude   = scrapy.Field()


