# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
from Teagardenshawksnestscraper.items import TeagardenshawksnestscraperItem
import requests
import re


class TeagardenshawksnestspiderSpider(scrapy.Spider):
    name = "teagardenshawksnestspider"
    allowed_domains = ["teagardenshawksnest.com"]
    start_urls = (
        'http://www.teagardenshawksnest.com/yesbookit?mod=site-search-res&f=1&nocss=1&many=18&sort=bud&arrival=&arrival_submit=&departure=&guests=',
        'http://www.teagardenshawksnest.com/yesbookit?mod=site-search-res&Category=Holiday&sort=bud&many=18&f=1&nocss=1&start=18',
        'http://www.teagardenshawksnest.com/yesbookit?mod=site-search-res&Category=Holiday&sort=bud&many=18&f=1&nocss=1&start=36',
        'http://www.teagardenshawksnest.com/yesbookit?mod=site-search-res&Category=Holiday&sort=bud&many=18&f=1&nocss=1&start=54',
        'http://www.teagardenshawksnest.com/yesbookit?mod=site-search-res&Category=Holiday&sort=bud&many=18&f=1&nocss=1&start=72',
        'http://www.teagardenshawksnest.com/yesbookit?mod=site-search-res&Category=Holiday&sort=bud&many=18&f=1&nocss=1&start=90',
        'http://www.teagardenshawksnest.com/yesbookit?mod=site-search-res&Category=Holiday&sort=bud&many=18&f=1&nocss=1&start=108',
    )

    def start_requests(self):
        for i in range(0,7):
            start_url = self.start_urls[i]
            yield scrapy.Request(start_url, self.parse)

    def parse(self, response):

        for apart_item in response.xpath('//article[@class="medium-6 large-4 columns"]'):
       	
            item_url = apart_item.xpath('div[@class="featured-property"]//div[@class="image-container"]/a/@href').extract()[0]
            description = apart_item.xpath('div[@class="featured-property"]//div[@class="details"]/text()').extract()
            price = apart_item.xpath('div[@class="featured-property"]//div[@class="featured-property-book"]//span[@class="price"]/text()').extract()
            url ="http://www.teagardenshawksnest.com" + item_url

            req = Request(url=url, callback=self.apart_detail, dont_filter=True)
            req.meta['check_url'] = url
            req.meta['description'] = description
            req.meta['price'] = price

            yield req            

    def apart_detail(self, response):
        self.logger.info("=======================================")
        self.logger.info(response)
        item = TeagardenshawksnestscraperItem()

        check_url = response.meta['check_url']
        description = response.meta['description']
        price = response.meta['price']
        item['URL'] = check_url
        item['Description'] = description
        item['Price'] = price

        ratingValue = response.xpath('//div[@class="row full-width"]/div[@class="name"]/span/meta[contains(@itemprop, "ratingValue")]/@content').extract()
        item['RatingValue'] = ratingValue

        reviewCount = response.xpath('//div[@class="row full-width"]/div[@class="name"]/span/meta[contains(@itemprop, "reviewCount")]/@content').extract()
        item['ReviewCount'] = reviewCount
        
        title = response.xpath('//div[@class="row full-width"]/div[@class="name"]/h1/text()').extract()
        item['Title'] = title

        test_body = response.xpath('//script[contains(text(), "var ipage_imgs")]/text()').extract_first()
        image_urls = re.search('var ipage_imgs_ = \[\,([\w\/\:\.\'\,\_\s]+)\]\,[\s]+mainimg', test_body, re.M|re.I|re.S).group(1)
        item['Images'] = ''.join(image_urls).strip()

        lat = re.search(r'lat = "(.*?)",', test_body, re.M|re.I|re.S).group(1)
        lon = re.search(r'lon = "(.*?)",', test_body, re.M|re.I|re.S).group(1)

        item['Latitude'] = lat
        item['Longitude'] = lon


        guests = ''.join(response.xpath('//div[@class="property-amenities"]/ul/li[1]/text()').extract()).strip()
        item['Guests'] = guests

        bed = ''.join(response.xpath('//div[@class="property-amenities"]/ul/li[2]/text()').extract()).strip()
        item['Beds'] = bed

        bathroom = ''.join(response.xpath('//div[@class="property-amenities"]/ul/li[3]/text()').extract()).strip()
        item['Bathrooms'] = bathroom

        car = ''.join(response.xpath('//div[@class="property-amenities"]/ul/li[4]/text()').extract()).strip()
        item['Car'] = car

        beddingConfig = response.xpath('//div[@class="small-12 columns"]/ul[@class="single-bedrooms"]/li/span[@class="bedroom-type"]/text()').extract()
        item['BeddingConfig'] = beddingConfig

        properties = ''.join(response.xpath('//div[@class="property-information"]//p/text()').extract()).strip()
        item['Properties'] = properties

        facilities = ''.join(response.xpath('//div[@class="property-facilities"]//ul/li//text()').extract()).strip()
        item['Facilities'] = facilities

        activities = ''.join(response.xpath('//div[@class="property-facilities"]/div[@class="row"]/p//text()').extract()).strip()

        item['Activities'] =activities
        
        yield item