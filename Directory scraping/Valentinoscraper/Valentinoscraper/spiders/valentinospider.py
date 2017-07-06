# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from Valentinoscraper.items import ValentinoscraperItem


class ValentinospiderSpider(scrapy.Spider):
    name = "valentinospider"
    allowed_domains = ["valentino.com"]
    start_urls = (
        'http://www.valentino.com/experience/it/pages/store-locator/#search/coords/53.92426306593819,7.300373559374975/ne/55.58577300344261,17.435261254687475/sw/52.26275312843377,-2.8345141359375248',
    )

    def __init__(self):

        self.temp_num = 0
        self.brand    = 'Valentino'

    def parse(self,response):

        for stores in response.xpath('//div[@class="storelocator-list-container"]/ul/li') :

            item = ValentinoscraperItem()

            item['City']        = ' '.join(stores.xpath('a/div[@class="address"]/text()').extract()).strip()
            item['Name']        = ' '.join(stores.xpath('a/h3/text()').extract()).strip()
            item['Address']     = ' '.join(stores.xpath('a/div[@class="address"]/text()').extract()).strip()
            item['Shoptype']    = ' '.join(stores.xpath('a/h3/text()').extract()).strip()
            item['Brand']       = self.brand

            yield item
