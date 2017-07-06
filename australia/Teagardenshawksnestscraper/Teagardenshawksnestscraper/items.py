# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TeagardenshawksnestscraperItem(scrapy.Item):

	Title         = scrapy.Field()
	URL           = scrapy.Field()
	Images        = scrapy.Field()
	Price         = scrapy.Field()
	Bathrooms     = scrapy.Field()
	Car           = scrapy.Field()
	Beds          = scrapy.Field()
	Guests        = scrapy.Field()
	Description   = scrapy.Field()
	RatingValue   = scrapy.Field()
	ReviewCount   = scrapy.Field()
	Latitude      = scrapy.Field()
	Longitude     = scrapy.Field()
	Properties    = scrapy.Field()
	Facilities    = scrapy.Field()
	Activities    = scrapy.Field()
	BeddingConfig = scrapy.Field()
