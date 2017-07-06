# -*- coding: utf-8 -*-
import scrapy
import useragent
from scrapy.http import Request, FormRequest
from Ftscraper.items import IncomesItem
import time, datetime, csv, random, base64, re, json
import sys
import MySQLdb
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

dbargs = settings.get('DB_CONNECT')    
db_server = settings.get('DB_SERVER')    
db = MySQLdb.connect(dbargs['host'], dbargs['user'], dbargs['passwd'], dbargs['db'])
cursor = db.cursor()

class IncomespiderSpider(scrapy.Spider):
    name = "incomespider"
    allowed_domains = ["ft.com"]

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

        with open('urlLists.csv') as csvfile:
            reader = csv.DictReader(csvfile)

            for listCount, row in enumerate(reader):

                Link = ''.join(row['Link']).strip()
                dbData = cursor.execute("SELECT secid FROM equities_data where Link='" + Link + "'")
                dbData = cursor.fetchall()
                if dbData:

                    secid =re.search(r'\d+', str(dbData)).group()

                    Symb = ''.join(row['Symb']).strip()
                    annualUrl = "https://markets.ft.com/data/equities/tearsheet/financials?s=" + Symb + "&subView=IncomeStatement&periodType=a"
                    req = self.set_proxies(annualUrl, self.getIncomesData)

                    req.meta['secid'] = secid
                    req.meta['Isfr'] = "1"
                    # req.meta['url'] = url

                    yield req

                    interimUrl = "https://markets.ft.com/data/equities/tearsheet/financials?s=" + Symb + "&subView=IncomeStatement&periodType=q"
                    req = self.set_proxies(interimUrl, self.getIncomesData)

                    req.meta['secid'] = secid
                    req.meta['Isfr'] = "2"

                    yield req
                # if listCount>3:
                    # return 

    def getIncomesData(self, response):
        self.logger.info("====== Get IncomesData =======")
        # c_url = response.meta['url']
        # print c_url

        secid = response.meta['secid']
        Isfr = response.meta['Isfr']
        item = IncomesItem()

        item['secid'] = secid
        item['Isfr'] = Isfr

        Lsdt_Label = ''.join(response.xpath('//table[@class="mod-ui-table"]/thead/tr/th[1]/text()').extract()).strip()
        item['Lsdt_Label'] = Lsdt_Label

        Col1_Label = ''.join(response.xpath('//table[@class="mod-ui-table"]/thead/tr/th[2]/text()').extract()).strip()
        item['Col1_Label'] = Col1_Label
        
        Col2_Label = ''.join(response.xpath('//table[@class="mod-ui-table"]/thead/tr/th[3]/text()').extract()).strip()
        item['Col2_Label'] = Col2_Label
        
        Col3_Label = ''.join(response.xpath('//table[@class="mod-ui-table"]/thead/tr/th[4]/text()').extract()).strip()
        item['Col3_Label'] = Col3_Label

        itemPaths = response.xpath('//table[@class="mod-ui-table"]/tr[contains(@class, "mod-ui-table__row--striped") or contains(@class, "mod-ui-table__row--highlight")]')
        for itemPath in itemPaths:
            
            Lsdt_Value = ''.join(itemPath.xpath('th/text()').extract()).strip()
            item['Lsdt_Value'] = Lsdt_Value

            Col1_Value = ''.join(itemPath.xpath('td[1]/text()').extract()).strip()
            item['Col1_Value'] = Col1_Value

            Col2_Value = ''.join(itemPath.xpath('td[2]/text()').extract()).strip()
            item['Col2_Value'] = Col2_Value

            Col3_Value = ''.join(itemPath.xpath('td[3]/text()').extract()).strip()
            item['Col3_Value'] = Col3_Value

            yield item            



