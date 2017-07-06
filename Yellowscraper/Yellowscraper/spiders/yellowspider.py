# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from Yellowscraper.items import YellowscraperItem


class YellowspiderSpider(scrapy.Spider):
    name = "yellowspider"
    allowed_domains = ["yellowpages.com"]
    start_urls = (
        'http://www.yellowpages.com/search?search_terms=tattoo+shop&geo_location_terms=Australian+Business+Park%2C+West+Palm+Beach%2C+FL',
    )

    def parse(self, response):

        for product in response.xpath('//div[@class="scrollable-pane"]/div[@class="search-results organic"]/div') :

            item = YellowscraperItem()

            title = ' '.join(product.xpath('div/div[@class="v-card"]/div[@class="info"]/h3[@class="n"]/a[@class="business-name"]/text()').extract()).strip()

            item['Title'] = title
            address1 = ' '.join(product.xpath('div/div[@class="v-card"]/div[@class="info"]/div[@class="info-section info-primary"]/p[@class="adr"]/span[@class="street-address"]/text()').extract()).strip()
            address2 = ' '.join(product.xpath('div/div[@class="v-card"]/div[@class="info"]/div[@class="info-section info-primary"]/p[@class="adr"]/span[@class="addressLocality"]/text()').extract()).strip()
            address3 = ' '.join(product.xpath('div/div[@class="v-card"]/div[@class="info"]/div[@class="info-section info-primary"]/p[@class="adr"]/span[@class="addressRegion"]/text()').extract()).strip()
            address = address1 + address2 + address3

            print(address)
            item['Address'] = address
            phone = ' '.join(product.xpath('div/div[@class="v-card"]/div[@class="info"]/div[@class="info-section info-primary"]/div[@class="phones phone primary"]/text()').extract()).strip()

            item['Phone'] = phone
            distance = ' '.join(product.xpath('div/div[@class="v-card"]/div[@class="info"]/div[@class="info-section info-secondary"]/div[@class="distance"]/text()').extract()).strip()

            item['Distance'] = distance
            category = ' '.join(product.xpath('div/div[@class="v-card"]/div[@class="info"]/div[@class="info-section info-secondary"]/div[@class="categories"]/a//text()').extract()).strip()

            item['Category'] = category

            yield item