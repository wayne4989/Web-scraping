# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PacificpalmsholidayscraperItem(scrapy.Item):

	Title       = scrapy.Field()
	URL         = scrapy.Field()
	Price       = scrapy.Field()
	Shower      = scrapy.Field()
	Car         = scrapy.Field()
	Beds        = scrapy.Field()
	Guests      = scrapy.Field()
	Description = scrapy.Field()
	Amenities   = scrapy.Field()
	Address     = scrapy.Field()
	Picture     = scrapy.Field()
	Reviews     = scrapy.Field()
	Latitude    = scrapy.Field()
	Longitude   = scrapy.Field()
