# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GreatoceanroadholidayscraperItem(scrapy.Item):
    
	Title         = scrapy.Field()
	URL           = scrapy.Field()
	Address       = scrapy.Field()
	Images        = scrapy.Field()
	Price         = scrapy.Field()
	Guests        = scrapy.Field()
	Car           = scrapy.Field()
	Beds          = scrapy.Field()
	Shower        = scrapy.Field()
	Amenities     = scrapy.Field()
	Description   = scrapy.Field()
	RatingValue   = scrapy.Field()
	ReviewCount   = scrapy.Field()
	Latitude      = scrapy.Field()
	Longitude     = scrapy.Field()
	Activities    = scrapy.Field()
	Experiences   = scrapy.Field()
	Services      = scrapy.Field()

