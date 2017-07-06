# -*- coding: utf-8 -*-
import scrapy
import useragent
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from Ftscraper.items import EquitiesItem
import time, datetime, csv, random, base64, re, json

class EquitiespiderSpider(scrapy.Spider):
    name = "equitiespider"
    useragent_lists = useragent.user_agent_list

    def set_proxies(self, url, callback, headers=None):

        req = Request(url=url, callback=callback, dont_filter=True, headers= headers)
        user_pass=base64.encodestring(b'user:password').strip().decode('utf-8')
        req.meta['proxy'] = "http://xxx.xxx.net:xxx"
        req.headers['Proxy-Authorization'] = 'Basic ' + user_pass
        user_agent = self.useragent_lists[random.randrange(0, len(self.useragent_lists))]
        req.headers['User-Agent'] = user_agent

        return req

    def start_requests(self):
        self.logger.info("=================== Start ===================")

        with open('urlLists.csv') as csvfile:
            reader = csv.DictReader(csvfile)

            for listCount, row in enumerate(reader):

                Link = ''.join(row['Link']).strip()
                CompanyName = ''.join(row['CompanyName']).strip()
                Country = ''.join(row['Country']).strip()
                Industry = ''.join(row['Industry']).strip()
                Symb = ''.join(row['Symb']).strip()
                # testUrl = "https://markets.ft.com/data/equities/tearsheet/profile?s=CAT:NYQ"
                url = "https://markets.ft.com/data/equities/tearsheet/profile?s=" + Symb

                req = self.set_proxies(url, self.getProfileData)
                # req = self.set_proxies(testUrl, self.getProfileData)

                req.meta['itemUrl'] = Link
                req.meta['itemCompany'] = CompanyName
                req.meta['itemCountry'] = Country
                req.meta['itemIndustry'] = Industry     

                yield req
                
                # if listCount > 5:

                #     return       

    def getProfileData(self, response):
        self.logger.info("====== getProfileData ======")

        itemUrl = response.meta['itemUrl']
        itemCompany = response.meta['itemCompany']
        itemIndustry = response.meta['itemIndustry']  
        itemCountry = response.meta['itemCountry']  

        item = EquitiesItem()

        item['Link'] = itemUrl 
        item['CompanyName'] = itemCompany
        item['Country'] = itemCountry        
        item['Industry'] = itemIndustry        

        Incorporated = ""
        Employees = ""
        Location = ""
        Phone = ""
        Fax = ""
        Website = ""
        
        description = ''.join(response.xpath('//div[@data-f2-app-id="mod-tearsheet-profile"]//p[@class="mod-tearsheet-profile-description mod-tearsheet-profile-section"]/text()').extract()).strip()
        item['About_Company'] = description
        # self.logger.info(description)

        statesLists = response.xpath('//ul[@class="mod-tearsheet-profile-stats mod-tearsheet-profile-section mod-tearsheet-profile__extra__content"]/li')
        
        for statesList in statesLists:
            label = ''.join(statesList.xpath('span[@class="mod-ui-data-list__label"]/span/text()').extract()).strip()
            if label=="":
                label = ''.join(statesList.xpath('span[@class="mod-ui-data-list__label"]/text()').extract()).strip()
            # self.logger.info(label)

            if label=="Revenue":
                Revenue = statesList.xpath('span//text()').extract()
                # self.logger.info(Revenue)

            elif label=="Net income":
                Net_income = statesList.xpath('span//text()').extract()
                # self.logger.info(Net_income)

            elif label=="Incorporated":
                Incorporated = ''.join(statesList.xpath('span[@class="mod-ui-data-list__value"]/text()').extract()).strip()
                item['Incorporate'] = Incorporated
                # self.logger.info(Incorporated)

            elif label=="Employees":
                Employees = ''.join(statesList.xpath('span[@class="mod-ui-data-list__value"]/text()').extract()).strip()
                item['Employees'] = Employees
                # self.logger.info(Employees)
        
        infoLists = response.xpath('//ul[@class="mod-tearsheet-profile-info mod-tearsheet-profile-section mod-tearsheet-profile__extra__content"]/li')
        for infoList in infoLists:
            label = ''.join(infoList.xpath('span[@class="mod-ui-data-list__label"]/text()').extract()).strip()

            # self.logger.info(label)

            if label=="Location":
                Location = ''.join(infoList.xpath('span[@class="mod-ui-data-list__value"]/address/span/text()').extract()).strip()
                item['Location'] = Location
                # self.logger.info(Location)

            elif label=="Phone":
                Phone = ''.join(infoList.xpath('span[@class="mod-ui-data-list__value"]/text()').extract()).strip()
                item['Phone'] =Phone
                # self.logger.info(Phone)

            elif label=="Fax":
                Fax = ''.join(infoList.xpath('span[@class="mod-ui-data-list__value"]/text()').extract()).strip()
                item['Fax'] = Fax
                # self.logger.info(Fax)

            elif label=="Website":
                Website = ''.join(infoList.xpath('span[@class="mod-ui-data-list__value"]/a/text()').extract()).strip()
                item['Website'] = Website
                # self.logger.info(Website)  

        yield item