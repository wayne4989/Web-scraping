# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
from Pacificpalmsholidayscraper.items import PacificpalmsholidayscraperItem
import requests
import re

class PacificpalmsholidayspiderSpider(scrapy.Spider):
    name = "pacificpalmsholidayspider"
    allowed_domains = ["pacificpalmsholidays.com.au"]
    start_urls = (
        'http://www.pacificpalmsholidays.com.au/yesbookit?mod=site-search-res&Category=Holiday&sort=bud&many=20&f=1&nocss=1&start=0',
        'http://www.pacificpalmsholidays.com.au/yesbookit?mod=site-search-res&Category=Holiday&sort=bud&many=20&f=1&nocss=1&start=20',
        'http://www.pacificpalmsholidays.com.au/yesbookit?mod=site-search-res&Category=Holiday&sort=bud&many=20&f=1&nocss=1&start=40',
        'http://www.pacificpalmsholidays.com.au/yesbookit?mod=site-search-res&Category=Holiday&sort=bud&many=20&f=1&nocss=1&start=60',
        'http://www.pacificpalmsholidays.com.au/yesbookit?mod=site-search-res&Category=Holiday&sort=bud&many=20&f=1&nocss=1&start=80',
        'http://www.pacificpalmsholidays.com.au/yesbookit?mod=site-search-res&Category=Holiday&sort=bud&many=20&f=1&nocss=1&start=100',
        'http://www.pacificpalmsholidays.com.au/yesbookit?mod=site-search-res&Category=Holiday&sort=bud&many=20&f=1&nocss=1&start=120',
        'http://www.pacificpalmsholidays.com.au/yesbookit?mod=site-search-res&Category=Holiday&sort=bud&many=20&f=1&nocss=1&start=140',
        'http://www.pacificpalmsholidays.com.au/yesbookit?mod=site-search-res&Category=Holiday&sort=bud&many=20&f=1&nocss=1&start=160',
    )
    def start_requests(self):
        for i in range(0,9):
            start_url = self.start_urls[i]
            yield scrapy.Request(start_url, self.parse)

    def parse(self, response):


        for apart_item in response.xpath('//article[@class="masonry-item"]'):
            item_url = apart_item.xpath('div/div[@class="results-thumb"]/a/@href').extract()[0]
            price = apart_item.xpath('div//div[@class="price"]/span/text()').extract()
            reviews = ''.join(apart_item.xpath('div/div[@class="results-thumb"]/span[@class=" rating-count f-right results-reviews"]/a/text()').extract()).strip()

            description = apart_item.xpath('div//div[@class="results-title"]/p[contains(@align, "justify")]/text()').extract()            
            url ="http://www.pacificpalmsholidays.com.au" + item_url

            req = Request(url=url, callback=self.apart_detail, dont_filter=True)
            req.meta['check_url'] = url
            req.meta['price'] = price
            req.meta['reviews'] = reviews
            req.meta['description'] = description

            yield req            

    def apart_detail(self, response):

        item = PacificpalmsholidayscraperItem()

        check_url = response.meta['check_url']
        item['URL'] = check_url

        price = response.meta['price']
        item['Price'] = price

        reviews = response.meta['reviews']
        if reviews:
            reviews=re.search(r'[\-\.0-9]+', reviews, re.M|re.I|re.S)
            item['Reviews'] = reviews.group(0)
        else:
            item['Reviews'] = ""

        description = response.meta['description']
        item['Description'] = description

        title = response.xpath('//div[@class="single-header"]/h1[@class="property-title"]/text()').extract()
        item['Title'] = title
        
        streetAddress = ''.join(response.xpath('//div[@class="single-header"]/span/span[contains(@itemprop, "streetAddress")]/text()').extract()).strip()
        addressLocality = ''.join(response.xpath('//div[@class="single-header"]/span/span[contains(@itemprop, "addressLocality")]/text()').extract()).strip()
        addressRegion = ''.join(response.xpath('//div[@class="single-header"]/span/span[contains(@itemprop, "addressRegion")]/text()').extract()).strip()
        postalCode = ''.join(response.xpath('//div[@class="single-header"]/span/span[contains(@itemprop, "postalCode")]/text()').extract()).strip()

        address = streetAddress + ", " + addressLocality + ", " + addressRegion + ", " + postalCode
        item['Address'] = address

        test_body = response.xpath('//script[contains(text(), "var ipage_imgs")]/text()').extract_first()
        image_urls = re.search('var ipage_imgs_ = \[\,([\w\/\:\.\'\,\_\s]+)\]\,[\s]+mainimg', test_body, re.M|re.I|re.S).group(1)
        item['Picture'] = image_urls

        lat = re.search(r'lat = "(.*?)",', test_body, re.M|re.I|re.S).group(1)
        lon = re.search(r'lon = "(.*?)",', test_body, re.M|re.I|re.S).group(1)

        item['Latitude'] = lat
        item['Longitude'] = lon

        data_detail = response.xpath('//div[@class="ninecol"]//ul[@class="single-amenities f-right"]')
        guests = ''.join(data_detail.xpath('li[1]/text()').extract()).strip()
        item['Guests'] = guests

        bed = ''.join(data_detail.xpath('li[2]/span/text()').extract()).strip()
        item['Beds'] = bed

        shower = ''.join(data_detail.xpath('li[3]/text()').extract()).strip()
        item['Shower'] = shower

        car = ''.join(data_detail.xpath('li[4]/text()').extract()).strip()
        item['Car'] = car

        amenities = response.xpath('//div[@class="row content cf"]/div[@class="ninecol"]/ul[1]/li/text()').extract()
        item['Amenities'] = amenities
        
        yield item