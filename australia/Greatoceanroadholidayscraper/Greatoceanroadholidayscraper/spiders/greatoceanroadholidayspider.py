# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
from Greatoceanroadholidayscraper.items import GreatoceanroadholidayscraperItem
import requests
import re

class GreatoceanroadholidayspiderSpider(scrapy.Spider):
    name = "greatoceanroadholidayspider"
    allowed_domains = ["greatoceanroadholidays.com.au"]
    start_urls = (
        'http://www.greatoceanroadholidays.com.au/',
    )

    def start_requests(self):

        for i in range(0,80):
            count = i*8
            url = 'http://www.greatoceanroadholidays.com.au/yesbookit?mod=site-search-res&Category=Holiday&many=8&f=1&nohead=1&nocss=1&start=%d' % count
            yield scrapy.Request(url, self.parse)

    def parse(self, response):


        for apart_item in response.xpath('//article[@class="masonry-item"]'):
            item_url = apart_item.xpath('div/div[@class="results-thumb"]/a/@href').extract()[0]
            price = apart_item.xpath('div//div[@class="price"]/span/text()').extract()

            description = apart_item.xpath('div//div[@class="results-title"]/p[@class="results-description"]/text()').extract()            
            url ="http://www.greatoceanroadholidays.com.au" + item_url

            req = Request(url=url, callback=self.apart_detail, dont_filter=True)
            req.meta['check_url'] = url
            req.meta['price'] = price
            req.meta['description'] = description

            yield req   

    def apart_detail(self, response):
        self.logger.info("=======================================")

        item = GreatoceanroadholidayscraperItem()

        check_url = response.meta['check_url']
        price = response.meta['price']
        description = ''.join(response.meta['description']).strip()

        item['URL'] = check_url
        item['Price'] = price
        item['Description'] = description

        ratingValue = ''.join(response.xpath('//div[@class="single-header"]/span[@class="results-reviews f-right"]/meta[contains(@itemprop, "ratingValue")]/@content').extract()).strip()
        if(ratingValue == "-average_rating-"):
        	item['RatingValue'] = ""
        else:
        	item['RatingValue'] = ratingValue

        reviewCount = ''.join(response.xpath('//div[@class="single-header"]/span[@class="results-reviews f-right"]/a/span/text()').extract()).strip()
        if(reviewCount == "-total_reviews-"):
        	item['ReviewCount'] = ""
        else:
        	item['ReviewCount'] = reviewCount

        title = response.xpath('//div[@class="single-header"]/h1/text()').extract()
        item['Title'] = title

        addresspath = response.xpath('div[@class="container lighter"]//div[@class="single-header"]/span[@class="f-left"]')

        streetAddress = ''.join(response.xpath('//div[@class="single-header"]/span[@class="f-left"]/span[contains(@itemprop, "streetAddress")]/text()').extract()).strip()
        addressLocality = ''.join(response.xpath('//div[@class="single-header"]/span[@class="f-left"]/span[contains(@itemprop, "addressLocality")]/text()').extract()).strip()
        addressRegion = ''.join(response.xpath('//div[@class="single-header"]/span[@class="f-left"]/span[contains(@itemprop, "addressRegion")]/text()').extract()).strip()
        postalCode = ''.join(response.xpath('//div[@class="single-header"]/span[@class="f-left"]/span[contains(@itemprop, "postalCode")]/text()').extract()).strip()

        address = streetAddress + ", " + addressLocality + ", " + addressRegion + ", " + postalCode
        item['Address'] = address

        test_body = response.xpath('//script[contains(text(), "var ipage_imgs")]/text()').extract_first()

        image_urls = re.search('var ipage_imgs_ = \[\,([\w\/\:\.\'\,\_\s]+)\]\,[\s]+mainimg', test_body, re.M|re.I|re.S)
        if image_urls:
            image_urls = image_urls.group(1)
            item['Images'] = image_urls

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


        amenities = response.xpath('//div[@class="row content cf"]/div[@class="ninecol"]/ul/li/text()').extract()
        item['Amenities'] = amenities

        detaildespaths = response.xpath('//div[@class="row content cf"]/div[@class="ninecol"]/h2')
        for detaildespath in detaildespaths:
            text = ''.join(detaildespath.xpath('text()').extract()).strip()
            self.logger.info(text)

            if(text=="Activities"):
                activities = detaildespath.xpath('following-sibling::p[1]/text()').extract()
                item['Activities'] = activities

            if(text=="Experiences"):
                experiences = detaildespath.xpath('following-sibling::p[1]/text()').extract()
                item['Experiences'] = experiences

            if(text=="Services"):
                services = detaildespath.xpath('following-sibling::p[1]/text()').extract()
                item['Services'] = services
        
        yield item    