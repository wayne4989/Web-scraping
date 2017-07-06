# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HouzzscraperItem(scrapy.Item):
# Haver & Skolnick LLC Architects
# Connecticut-Based, Preferred Architectural Firm
# (860) 650-1537
# Architects & Building Designers
# Contact: CHARLES HAVER
# Location: Roxbury, CT 06783
# License Number: CT: ARI.0009540; NY: 02394-1
# Typical Job Costs: $500,000 - 15,000,000
    Name = scrapy.Field()
    Profile = scrapy.Field()
    Phone = scrapy.Field()
    Profession = scrapy.Field()
    Contact = scrapy.Field()
    Location = scrapy.Field()
    License = scrapy.Field()
    Price = scrapy.Field()
