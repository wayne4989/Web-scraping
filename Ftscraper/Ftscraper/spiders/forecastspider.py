# -*- coding: utf-8 -*-
import scrapy
import useragent
from scrapy.http import Request, FormRequest
from Ftscraper.items import ForecastsItem
import time, datetime, csv, random, base64, re, json
import sys
import MySQLdb
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

dbargs = settings.get('DB_CONNECT')    
db_server = settings.get('DB_SERVER')    
db = MySQLdb.connect(dbargs['host'], dbargs['user'], dbargs['passwd'], dbargs['db'])
cursor = db.cursor()

class ForecastspiderSpider(scrapy.Spider):
    name = "forecastspider"
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
                    url = "https://markets.ft.com/data/equities/tearsheet/forecasts?s=" + Symb
                    req = self.set_proxies(url, self.getForecastData)

                    req.meta['secid'] = secid

                    yield req
                # if listCount>2:
                #     return 
    def getForecastData(self, response):
        self.logger.info("====== Get Forecast Data =======")

        i = datetime.datetime.now()
        currentDate =  "%s-%s-%s" % (i.year, i.month, i.day)
        item = ForecastsItem()

        secid = response.meta['secid']
        item['secid'] = secid
        item['Date'] = currentDate

        itemPaths = response.xpath('//table[@class="mod-ui-table mod-ui-table--colored"]/tbody/tr')
        if itemPaths:
            print "---- True -----"

            for itemPath in itemPaths:
                print "------------"
                text = ''.join(itemPath.xpath('td[1]/span/span/text()').extract()).strip()
                print text
        
                if text=="Buy":
                    # item['Buy'] = ''.join(itemPath.xpath('td[3]/text()').extract()).strip()
                    Buy = ''.join(itemPath.xpath('td[3]/text()').extract()).strip()
                    item['Buy'] = Buy
                    print Buy
                elif text=="Outperform":
                    # item['Outperform'] = ''.join(itemPath.xpath('td[3]/text()').extract()).strip()
                    Outperform = ''.join(itemPath.xpath('td[3]/text()').extract()).strip()
                    item['Outperform'] = Outperform
                    print Outperform
            
                elif text=="Hold":
                    # item['Hold'] = ''.join(itemPath.xpath('td[3]/text()').extract()).strip()
                    Hold = ''.join(itemPath.xpath('td[3]/text()').extract()).strip()
                    item['Hold'] = Hold
                    print Hold
            
                elif text=="Underperform":
                    # item['Under'] = ''.join(itemPath.xpath('td[3]/text()').extract()).strip()
                    Under = ''.join(itemPath.xpath('td[3]/text()').extract()).strip()
                    item['Under'] = Under
                    print Under
            
                elif text=="Sell":
                    # item['Sell'] = ''.join(itemPath.xpath('td[3]/text()').extract()).strip()
                    Sell = ''.join(itemPath.xpath('td[3]/text()').extract()).strip()
                    item['Sell'] = Sell
                    print Sell
                
            yield item
