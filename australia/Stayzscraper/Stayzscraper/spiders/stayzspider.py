# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
from Stayzscraper.items import StayzscraperItem
import requests
import re


class StayzspiderSpider(scrapy.Spider):
    name = "stayzspider"
    allowed_domains = ["stayz.com.au"]
    start_urls = (
        'https://www.stayz.com.au/accommodation/nsw/north-coast',
    )

    def parse(self, response):
        self.logger.info("=======================================")
        
        aparts = response.xpath('//div[@class="c-property-tile__img-wrapper"]')
        for apart in aparts:
            apart_path = apart.xpath('a[@class="c-property-tile__link"]/@href').extract()[0]
            self.logger.info(apart_path)
            url = "https://www.stayz.com.au" + apart_path

            req = Request(url=url, callback=self.apart_detail, dont_filter=True)
            req.meta['check_url'] = url
            yield req

        next_page = response.xpath('//nav[@class="c-pagination"]/ul/li[7]/a[@class="c-pagination__link c-pagination__link--direction"]/@href').extract()[0]
        if next_page:
            next_page_url = "https://www.stayz.com.au" + next_page
            yield Request(url=next_page_url, callback=self.parse, dont_filter=True)

    def apart_detail(self, response):

        item = StayzscraperItem()

        check_url = response.meta['check_url']
        item['URL'] = check_url

        title = response.xpath('//header[@class="u-spacing--bottom--large u-text--center"]/h1/text()').extract()
        item['Title'] = title

        rated = ''.join(response.xpath('//p[@class="u-padded--vertical--small"]//span[@class="u-text--sr-only"]/text()').extract()).strip()
        item['Rated'] = rated

        reviews = ''.join(response.xpath('//p[@class="u-padded--vertical--small"]//small[@class="u-display--block"]/text()').extract()).strip()
        if reviews:
            reviews=re.search(r'[\-\.0-9]+', reviews, re.M|re.I|re.S)
            item['Reviews'] = reviews.group(0)
        else:
            item['Reviews'] = ""

        price = response.xpath('//div[@class="c-quote c-quote--mini u-hidden--desk u-transform-none"]//p[2]//span[@class="u-h1"]/text()').extract()
        if price:
            item['Price'] = price[0]
        else:
            price = response.xpath('//div[@class="c-quote c-quote--mini u-hidden--desk u-transform-none"]//p//span[@class="u-h1"]/text()').extract()
            item['Price'] = price[0]

        detail_apart = response.xpath('//div[@class="c-facets c-facets--inline"]//span[@class="c-facet__label u-display--block"]/text()').extract()
        guests = detail_apart[0]
        guests=re.search(r'[\-\.0-9]+', guests, re.M|re.I|re.S)
        item['Guests'] = guests.group(0)

        bedrooms = detail_apart[1]
        bedrooms=re.search(r'[\-\.0-9]+', bedrooms, re.M|re.I|re.S)
        item['Bedrooms'] = bedrooms.group(0)

        beds = detail_apart[2]
        beds=re.search(r'[\-\.0-9]+', beds, re.M|re.I|re.S)
        item['Beds'] = beds.group(0)

        bathrooms = detail_apart[3]
        bathrooms=re.search(r'[\-\.0-9]+', bathrooms, re.M|re.I|re.S)
        item['Bathrooms'] = bathrooms.group(0)

        description = ''.join(response.xpath('//div[@class="c-hidden-content c-hidden-content--hidden"]/p/text()').extract()).strip()
        item['Description'] = description

        features = ''.join(response.xpath('//div[@class="o-media__body"]/p[@class="u-spacing--flush"]/text()').extract()).strip()
        item['Features'] = features

        image_url = response.xpath('//div[@class="c-gallery__images u-transform-none"]//img/@data-lazy').extract()
        item['Picture'] = image_url


        latitude = response.xpath('//div[@class="c-map__container"]/@lat').extract()
        longitude = response.xpath('//div[@class="c-map__container"]/@lng').extract()
        item['Latitude'] = latitude
        item['Longitude'] = longitude

        yield item