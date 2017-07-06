# -*- coding: utf-8 -*-
import scrapy
import proxylist
import useragent
import re
from scrapy.http import Request, FormRequest
from Vrboscraper.items import VrboscraperItem
import time, re, random, base64, datetime
import requests
import csv, json
import sys
from time import sleep
from copy import deepcopy

class VrbospiderSpider(scrapy.Spider):
    name = "vrbospider"
    allowed_domains = ["vrbo.com"]
    start_urls = (
        # 'http://www.vrbo.com/',
        'http://www.vrbo.com/vacation-rentals/usa?sleeps=4-plus&from-date=2017-06-15&to-date=2017-06-22&page=1',
        )

    proxy_lists = proxylist.proxys
    useragent_lists = useragent.user_agent_list

    base_url = "http://www.vrbo.com"

    def set_proxies(self, url, callback):

        req = Request(url=url, callback=callback, dont_filter=True)

        proxy_url = self.proxy_lists[random.randrange(0,len(self.proxy_lists))]
        user_pass=base64.encodestring(b'user:password').strip().decode('utf-8')      
        req.meta['proxy'] = "http://" + proxy_url
        req.headers['Proxy-Authorization'] = 'Basic ' + user_pass
        user_agent = self.useragent_lists[random.randrange(0, len(self.useragent_lists))]
        req.headers['User-Agent'] = user_agent

        return req

    def start_requests(self):
        self.logger.info("======================== Start =====================")

        start_url = "https://www.vrbo.com/vacation-rentals?page=1&region=1875&from-date=2017-06-15&to-date=2017-06-22&searchTermContext=2df1c17a-f770-4033-bd2b-0e7a97a09a00&searchTermUuid=2df1c17a-f770-4033-bd2b-0e7a97a09a00&sort+by=Price%2FDescending&sleeps=4-plus"
        reqa = self.set_proxies(start_url, self.getData)
        yield reqa

    def getData(self, response):

        self.logger.info("=============== Get data ====================")

        list_divs = response.xpath('//div[@class="box-content"]')
        list_divs1 = response.xpath('//div[@class="js-hitContent simple-hit__content row"]')
        lis = response.xpath('//li[@class="row list-group-item  property-ipmolb"]')

        if len(lis) > 0:

            for div in lis:
                path_url = div.xpath('.//a[@class="altlisting-title searchviewtopdp-hybridlist"]/@href').extract_first()
                self.logger.info("------- lis -------")

                url = self.base_url + path_url
                req = self.set_proxies(url, self.parseData)
                req.meta["url"] = url
                req.meta["dataid"] = path_url
                yield req

        elif len(list_divs) > 0:

            for div in list_divs:
                path_url = div.xpath('.//a[@class="hit-url listing-url js-hitLink"]/@href').extract_first()
                self.logger.info("------- list_divs -------")

                url = self.base_url + path_url
                req = self.set_proxies(url, self.parseData)
                req.meta["url"] = url
                req.meta["dataid"] = path_url
                yield req

        elif len(list_divs1) > 0:

            for div in list_divs1:
                path_url = div.xpath('.//a[@class="hit-url listing-url js-hitLink"]/@href').extract_first()
                self.logger.info("------- list_divs1 -------")

                url = self.base_url + path_url
                req = self.set_proxies(url, self.parseData)
                req.meta["url"] = url
                req.meta["dataid"] = path_url

                yield req                

        next_div = response.xpath('//link[@rel="next"]')
        
        if len(next_div) > 0:
            path_url = next_div.xpath("@href").extract_first()
            url = self.base_url + path_url
            print "Next->", url
            req = self.set_proxies(url, self.getData)
            req.meta["url"] = url
            yield req

    def parseData(self, response):
        self.logger.info("=============== Parse data ====================")

        sleeps = ""
        bedrooms = ""
        bathrooms = ""
        property_type = ""
        minimum_Stay = ""
        owner = ""
        propertyManger = ""

        url = response.meta['url']
        self.logger.info(url)

        location = ''.join(response.xpath('//ol[@class="breadcrumb breadcrumb-gt-header hidden-xs js-breadcrumb"]/li[@class="last"]/a/text()').extract()).strip()

        if len(location)>0:
            item = VrboscraperItem()
            item['Link'] = url

            self.logger.info(location)
            item['Location'] = location            

            data_id = ''.join(response.xpath('//ol[@class="breadcrumb breadcrumb-gt-header hidden-xs js-breadcrumb"]/li[@class="unlinked"]/text()').extract()).strip()
            self.logger.info(data_id)
            item['ID'] = data_id

            description = ''.join(response.xpath('//div[@class="pdp-headline-container container hidden-xs js-headlineContainer"]//h1[@class="listing-headline "]/span/text()').extract()).strip()
            self.logger.info(description)
            item['Description'] = description
            
            subPaths = response.xpath('//table[@class="table table-striped amenity-table"]/tbody/tr')
            for data_tr in subPaths:

                first_td = data_tr.xpath("td")
                data_level = first_td.xpath("text()").extract_first()

                if( data_level == "Sleeps" ):
                    self.logger.info("----------- sleeps -----------")

                    sleeps = first_td.xpath("following-sibling::td/text()").extract_first()
                    item['Sleeps'] = sleeps
                    self.logger.info(sleeps)

                elif( data_level == "Bedrooms" ):
                    self.logger.info("----------- Bedrooms -----------")

                    bedrooms = first_td.xpath("following-sibling::td/text()").extract_first()
                    item['Bedrooms'] = bedrooms
                    self.logger.info(bedrooms)

                elif( data_level == "Bathrooms" ):
                    self.logger.info("----------- Bathrooms -----------")

                    bathrooms = first_td.xpath("following-sibling::td/text()").extract_first()
                    item['Bathrooms'] = bathrooms
                    self.logger.info(bathrooms)

                elif( data_level == "Property type" ):
                    self.logger.info("----------- Property type -----------")

                    property_type = first_td.xpath("following-sibling::td/text()").extract_first()
                    item['Property'] = property_type
                    self.logger.info(property_type)

                elif( data_level == "Minimum Stay" ):
                    self.logger.info("----------- Minimum Stay -----------")

                    minimum_Stay = first_td.xpath("following-sibling::td/text()").extract_first()
                    item['Minimum_Stay'] = minimum_Stay
                    self.logger.info(minimum_Stay)

            persons = response.xpath('//div[@class="summary-subtitle"]')

            for person in persons:
                
                text = ''.join(person.xpath('text()').extract()).strip()

                if text=="Owner":
                    self.logger.info("--------- Owner --------")
                    owner = ''.join(response.xpath('//span[@class="owner-name"]/text()').extract()).strip()
                    item['Owner'] = owner
                    self.logger.info(owner)

                elif text=="Property Manager":
                    self.logger.info("--------- Property Manager --------")
                    propertyManger = ''.join(response.xpath('//span[@class="owner-name"]/text()').extract()).strip()
                    item['Property_Manager'] = propertyManger
                    self.logger.info(propertyManger)

            spuPath = response.xpath('//div[@class="quotebar-buttons quotebar-buttons-row js-quoteBar buttons-inside-pricebar sticky-cta"]')      
            spu = spuPath.xpath('div[@class="quotebar-buttons-inner js-stickyCTA"]/ul[@class="nav pdp-fav-share-nav nav-icon-links "]/li[@class="dropdown favorite-button js-favoriteButtonView"]/@data-spu').extract_first()
            getPrice_url = "https://www.vrbo.com/ajax/olb/rates?arrivalDate=06/15/2017&departureDate=06/22/2017&transactionId=&adultsCount=4&childrenCount=0&petIncluded=false&spu=%s" %(spu)
            r = requests.get(getPrice_url)

            json_data = r.json()

            price = json_data['averageNightly']
            item['Rate_Night'] = price        

            yield item

        else:

            item = VrboscraperItem()

            item['Link'] = url

            dataid = response.meta['dataid']
            data_id = dataid.replace("/","")
            data_id = "Rental " + data_id
            self.logger.info(data_id)
            item['ID'] = data_id


            property_name = ''.join(response.xpath('//div[@class="content-top clearfix"]/h1/text()').extract()).strip()
            self.logger.info(property_name)
            item['Description'] = property_name

            details = response.xpath("//div[@class='splitter-group']/ul/li")

            for row in details:
                name_field = ''.join(row.xpath('b/text()').extract_first()).strip()
                if name_field == "Minimum stay:":
                    minimum_Stay = ''.join(row.xpath('span//text()').extract())
                    item['Minimum_Stay'] = minimum_Stay

                    self.logger.info(minimum_Stay)

                elif name_field == "Sleeps:":
                    sleeps = ''.join(row.xpath('span//text()').extract())
                    item['Sleeps'] = sleeps

                    self.logger.info(sleeps)

                elif name_field == "Bedrooms:":
                    bedrooms = ''.join(row.xpath('span//text()').extract())
                    item['Bedrooms'] = bedrooms

                    self.logger.info(bedrooms)

                elif name_field == "Bathrooms:":
                    bathrooms = ''.join(row.xpath('span//text()').extract())
                    item['Bathrooms'] = bathrooms

                    self.logger.info(bathrooms)

                elif name_field == "Property type:":
                    property_type = ''.join(row.xpath('span//text()').extract())
                    item['Property'] = property_type

                    self.logger.info(property_type)

            location = ''.join(response.xpath('//input[@class="searchform2-term form-control"]/@value').extract()[0]).strip()
            self.logger.info(location)
            item['Location'] = location            

            flag = re.search("data\-isownermanaged=\"(.*?)\"", response.body, re.I|re.S|re.M).group(1)
            self.logger.info(flag)

            if flag=="True":
                self.logger.info("Owner")
                owner = ''.join(response.xpath('//input[@id="ContactDisplayName"]/@value').extract()).strip()
                item['Owner'] = owner

                self.logger.info(owner)

            elif flag=="False":
                self.logger.info("Property")

                propertyManger = ''.join(response.xpath('//input[@id="ContactDisplayName"]/@value').extract()).strip()
                item['Property_Manager'] = propertyManger

                self.logger.info(propertyManger)

            spu = response.xpath('//span[@class="button-icon small favorite"]/@data-spu').extract_first()
            getPrice_url = "https://www.vrbo.com/ajax/olb/rates?arrivalDate=06/15/2017&departureDate=06/22/2017&transactionId=&adultsCount=4&childrenCount=0&petIncluded=false&spu=%s" %(spu)
            r = requests.get(getPrice_url)

            json_data = r.json()

            price = json_data['averageNightly']
            item['Rate_Night'] = price  


            yield item

    def getPrice(self, response):

        item = VrboscraperItem()

        url = response.meta['url']
        location = response.meta['location']
        data_id = response.meta['data_id']
        description = response.meta['description']
        sleeps = response.meta['sleeps']
        bedrooms = response.meta['bedrooms']
        bathrooms = response.meta['bathrooms']
        property_type = response.meta['property_type']
        minimum_Stay = response.meta['minimum_Stay']
        owner = response.meta['owner']
        propertyManger = response.meta['Property_Manager']

        json_data = json.loads(response.body_as_unicode())

        price = json_data['averageNightly']

        item['Link'] = url
        item['Location'] = location            
        item['Description'] = description
        item['ID'] = data_id
        item['Sleeps'] = sleeps
        item['Bedrooms'] = bedrooms
        item['Bathrooms'] = bathrooms
        item['Property'] = property_type
        item['Minimum_Stay'] = minimum_Stay
        item['Owner'] = owner
        item['Property_Manager'] = propertyManger
        item['Rate_Night'] = price        

        yield item