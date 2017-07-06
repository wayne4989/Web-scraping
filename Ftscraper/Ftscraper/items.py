# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EquitiesItem(scrapy.Item):
    # define the fields for your item here like:
    CompanyName = scrapy.Field()
    Link = scrapy.Field()
    Industry = scrapy.Field()
    Country = scrapy.Field()
    About_Company = scrapy.Field()
    Incorporate = scrapy.Field()
    Location = scrapy.Field()
    Phone = scrapy.Field()
    Fax = scrapy.Field()
    Website = scrapy.Field()
    Employees = scrapy.Field()    

class GetUrlItem(scrapy.Item):
    # define the fields for your item here like:
    CompanyName = scrapy.Field()
    Link = scrapy.Field()
    Industry = scrapy.Field()
    Country = scrapy.Field()
    Symb = scrapy.Field()

class SymbolsItem(scrapy.Item):

    Symbol = scrapy.Field()
    Market = scrapy.Field()
    secid = scrapy.Field()

class DirectorsItem(scrapy.Item):

    secid = scrapy.Field()
    Name = scrapy.Field()
    Title = scrapy.Field()
    Compensation = scrapy.Field()
    Age = scrapy.Field()
    Since = scrapy.Field()

class DealingsItem(scrapy.Item):

    secid = scrapy.Field()
    Date = scrapy.Field()
    Type = scrapy.Field()
    Name = scrapy.Field()
    Title = scrapy.Field()
    Shares = scrapy.Field()
    Pershare = scrapy.Field()
    Dealsize = scrapy.Field()

class IncomesItem(scrapy.Item):

    secid = scrapy.Field()
    Isfr = scrapy.Field()
    Lsdt_Label = scrapy.Field()
    Col1_Label = scrapy.Field()
    Col2_Label = scrapy.Field()
    Col3_Label = scrapy.Field()
    Lsdt_Value = scrapy.Field()
    Col1_Value = scrapy.Field()
    Col2_Value = scrapy.Field()
    Col3_Value = scrapy.Field()

class CashFlowsItem(scrapy.Item):

    secid = scrapy.Field()
    Cffr = scrapy.Field()
    Cfdt_Label = scrapy.Field()
    Col1_Label = scrapy.Field()
    Col2_Label = scrapy.Field()
    Col3_Label = scrapy.Field()
    Cfdt_Value = scrapy.Field()
    Col1_Value = scrapy.Field()
    Col2_Value = scrapy.Field()
    Col3_Value = scrapy.Field()

class BalancesItem(scrapy.Item):

    secid = scrapy.Field()
    Bsfr = scrapy.Field()
    Bsdt_Label = scrapy.Field()
    Col1_Label = scrapy.Field()
    Col2_Label = scrapy.Field()
    Col3_Label = scrapy.Field()
    Bsdt_Value = scrapy.Field()
    Col1_Value = scrapy.Field()
    Col2_Value = scrapy.Field()
    Col3_Value = scrapy.Field()

class ForecastsItem(scrapy.Item):

    secid = scrapy.Field()
    Date = scrapy.Field()
    Buy = scrapy.Field()
    Outperform = scrapy.Field()
    Hold = scrapy.Field()
    Under = scrapy.Field()
    Sell = scrapy.Field()

class HistoricalItem(scrapy.Item):

    secid = scrapy.Field()
    Date = scrapy.Field() 
    Open = scrapy.Field()
    High = scrapy.Field()
    Low = scrapy.Field()
    Close = scrapy.Field()
    Volume = scrapy.Field()    