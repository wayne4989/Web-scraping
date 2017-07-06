# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DatagrapplescraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    deltaspread = scrapy.Field()
    vardate = scrapy.Field()
    spread = scrapy.Field()
    varid = scrapy.Field()
    vardur = scrapy.Field()
    dailyvol = scrapy.Field()
    # payload_check = scrapy.Field()

    # MinSpread = scrapy.Field()
    # IsOkSpread = scrapy.Field()
    # DeltaUpfront = scrapy.Field()
    # Name = scrapy.Field()
    # DtccCertainty = scrapy.Field()
    # Spread2 = scrapy.Field()
    # ParentName = scrapy.Field()
    # MaxSpread = scrapy.Field()
    # DataCertainty =scrapy.Field()
    # IdNode = scrapy.Field()
    # DeltaSpread2 = scrapy.Field()
    # OpenVolume = scrapy.Field()
    # LongName = scrapy.Field()
    # NodeType = scrapy.Field()
    # DailyVol = scrapy.Field()
    # Upfront = scrapy.Field()
    # IdParent = scrapy.Field()