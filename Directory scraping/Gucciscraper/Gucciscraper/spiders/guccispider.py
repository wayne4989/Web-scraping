# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from Gucciscraper.items import GucciscraperItem
import re

class GuccispiderSpider(scrapy.Spider):
    name = "guccispider"
    allowed_domains = ["gucci.com"]
    start_urls = (
        'https://www.gucci.com/int/en/store-finder',
    )

    def __init__(self):

        self.temp_num = 0
        self.brand    = 'Gucci'

    def parse(self,response):

        for stores in response.xpath('//div[@class="store-locator-cards"]/div[contains(@class, "store-locator-card location")]') :

            item = GucciscraperItem()

            item['Latitute']  = stores.xpath('@data-latitude').extract()[0]

            item['Longitude'] = stores.xpath('@data-longitude').extract()[0]

            city  = ' '.join(stores.xpath('div[@class="store-info"]/div[@class="store-info-column"]/p/text()').extract()).strip()
            city_text  = city.replace("\n","")
            city_text1 = city_text.replace(" 							", " ")
            item['City']    = city_text1
            item['Address'] = city_text1

            name = ' '.join(stores.xpath('div[@class="store-info"]/div[@class="store-info-column"]/h3/a/text()').extract()).strip()
            item['Name']     = name
            item['Shoptype'] = name

            item['Brand']    = self.brand

            yield item