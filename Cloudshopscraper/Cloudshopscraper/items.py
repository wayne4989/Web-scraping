# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CloudshopscraperItem(scrapy.Item):

    Company_Name          = scrapy.Field()
    Address_1             = scrapy.Field()
    Address_2             = scrapy.Field()
    City                  = scrapy.Field()
    Country               = scrapy.Field()
    Postal_Code           = scrapy.Field()
    State_Province        = scrapy.Field()
    Application_Category  = scrapy.Field()
    Target_Industry       = scrapy.Field()
    Key_Differentiators   = scrapy.Field()
    Sample_Customer_Names = scrapy.Field()
    Year_Founded          = scrapy.Field()
    Public_Private        = scrapy.Field()
    Company_Phone         = scrapy.Field()
    Company_Website       = scrapy.Field()
    Company_Email         = scrapy.Field()
    Check_url             = scrapy.Field()
    Category              = scrapy.Field()