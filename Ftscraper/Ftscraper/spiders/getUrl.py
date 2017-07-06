# -*- coding: utf-8 -*-
import scrapy
import useragent
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from Ftscraper.items import GetUrlItem
import time, datetime, csv, random, base64, re, json

class GeturlSpider(scrapy.Spider):
    name = "getUrl"
    allowed_domains = ["ft.com"]
    start_urls = (
        'https://markets.ft.com/data/equities/results',
    )

    
    useragent_lists = useragent.user_agent_list

    def set_proxies(self, url, callback, headers=None):

        req = Request(url=url, callback=callback, dont_filter=True, headers= headers)
        user_pass=base64.encodestring(b'user:password').strip().decode('utf-8')
        req.meta['proxy'] = "http://xxx.xxx.net:xxx"
        req.headers['Proxy-Authorization'] = 'Basic ' + user_pass
        user_agent = self.useragent_lists[random.randrange(0, len(self.useragent_lists))]
        req.headers['User-Agent'] = user_agent

        return req

    def parse(self, response):
        self.logger.info("=================== Start ===================")
        getNumber = ''.join(response.xpath('//li[@aria-disabled="false"]/preceding-sibling::li[1]/text()').extract()).strip()
        # self.logger.info(getNumber)
        # return

        for page in range(1,int(getNumber)+1):
            print "---------" + str(page) + "----------"
            url = "https://markets.ft.com/data/equities/ajax/updateScreenerResults?data=%5B%7B%22ArgsOperator%22%3Anull%2C%22ValueOperator%22%3Anull%2C%22Arguments%22%3A%5B%5D%2C%22Clauses%22%3A%5B%5D%2C%22ClauseGroups%22%3A%5B%5D%2C%22Field%22%3A%22RCCCountryCode%22%2C%22Identifiers%22%3Anull%2C%22Style%22%3Anull%7D%2C%7B%22ArgsOperator%22%3Anull%2C%22ValueOperator%22%3Anull%2C%22Arguments%22%3A%5B%5D%2C%22Clauses%22%3A%5B%5D%2C%22ClauseGroups%22%3A%5B%5D%2C%22Field%22%3A%22RCCICBIndustryCode%22%2C%22Identifiers%22%3Anull%2C%22Style%22%3Anull%7D%5D&page=" + str(page) + "&currencyCode=GBP&sort=%7B%22field%22%3A%22RCCFTStandardName%22%2C%22direction%22%3A%22ascending%22%7D"
            
            req = self.set_proxies(url, self.getMainData)

            yield req  
            # return        

    def getMainData(self, response):
        self.logger.info("====== getMainData ======")
        item = GetUrlItem()

        json_data = json.loads(response.body)
        htmlText = Selector(text=json_data["html"])
        itemPaths = htmlText.xpath('//table[@class="mod-ui-table mod-ui-table--freeze-pane"]/tr')


        for itemPath in itemPaths:

            itemUrl = "https:" + ''.join(itemPath.xpath('td[1]/a/@href').extract()).strip()
            item['Link'] = itemUrl 
            self.logger.info(itemUrl)

            itemSym = ''.join(itemPath.xpath('td[1]/a/span[@class="mod-ui-hide-small-above"]/text()').extract()).strip()
            item['Symb'] = itemSym
            self.logger.info(itemSym)

            itemCompany = ''.join(itemPath.xpath('td[1]/a/span[@class="mod-ui-hide-xsmall"]/text()').extract()).strip()
            
            item['CompanyName'] = itemCompany
            self.logger.info(itemCompany)

            itemCountry = ''.join(itemPath.xpath('td[2]/text()').extract()).strip()
            item['Country'] = itemCountry        
            self.logger.info(itemCountry)

            itemIndustry = ''.join(itemPath.xpath('td[3]/text()').extract()).strip()
            item['Industry'] = itemIndustry       
            self.logger.info(itemIndustry)

            yield item





