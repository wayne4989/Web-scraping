# -*- coding: utf-8 -*-
import scrapy
import useragent
from scrapy.http import Request, FormRequest
from Ftscraper.items import HistoricalItem
from scrapy.selector import Selector
import time, datetime, csv, random, base64, re, json
import sys
import MySQLdb
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

dbargs = settings.get('DB_CONNECT')    
db_server = settings.get('DB_SERVER')    
db = MySQLdb.connect(dbargs['host'], dbargs['user'], dbargs['passwd'], dbargs['db'])
cursor = db.cursor()

class HistoricalspiderSpider(scrapy.Spider):
    name = "historicalspider"
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
                    url = "https://markets.ft.com/data/equities/tearsheet/historical?s=" + Symb
                    req = self.set_proxies(url, self.getHistoricalData)

                    req.meta['secid'] = secid

                    yield req
                # if listCount>2:
                    # return 
    def getHistoricalData(self, response):
        self.logger.info("====== getHistoricalData ======")
        secid = response.meta['secid']

        getParams = ''.join(response.xpath('//div[@data-module-name="HistoricalPricesApp"]/@data-mod-config').extract()).strip()
        if getParams:
            
            getParam1 = re.search(r'"inception":"(.*?)"', getParams, re.M|re.I|re.S)
            inception = getParam1.group(1).split("T")[0]
            getParam2 = re.search(r'"symbol":"(.*?)"', getParams, re.M|re.I|re.S)
            symbol = getParam2.group(1)        

            startDate = datetime.datetime.strptime(inception, "%Y-%m-%d")

            currDate = datetime.datetime.now()

            between = currDate.year - startDate.year

            for count in range(1, int(between)):

                sDate = "%s %s %s" % (startDate.year, startDate.month, startDate.day)
                nextDate = startDate.replace(startDate.year + int(count))

                eDate = "%s %s %s" % (nextDate.year, nextDate.month, nextDate.day)
                            
                url = "https://markets.ft.com/data/equities/ajax/get-historical-prices?startDate=" + sDate + "&endDate=" + eDate + "&symbol=" + str(symbol)
                req = self.set_proxies(url, self.getData)
                req.meta['secid'] = secid

                yield req

            sDate = "%s %s %s" % (nextDate.year, nextDate.month, nextDate.day)

            eDate = "%s %s %s" % (currDate.year, currDate.month, currDate.day)

            url = "https://markets.ft.com/data/equities/ajax/get-historical-prices?startDate=" + sDate + "&endDate=" + eDate + "&symbol=" + str(symbol)
            req = self.set_proxies(url, self.getData)
            req.meta['secid'] = secid

            yield req

    def getData(self, response):
        self.logger.info("====== getData ======")
        item = HistoricalItem()
        secid = response.meta['secid']

        json_data = json.loads(response.body)
        htmlText = Selector(text=json_data["html"])

        item['secid'] = secid
        itemPaths = htmlText.xpath('//tr')

        for itemPath in itemPaths:
            Date = ''.join(itemPath.xpath('td[1]/span[1]/text()').extract()).strip()
            item['Date'] = Date
            
            Open = ''.join(itemPath.xpath('td[2]/text()').extract()).strip()
            item['Open'] = Open
            
            High = ''.join(itemPath.xpath('td[3]/text()').extract()).strip()
            item['High'] = High
            
            Low = ''.join(itemPath.xpath('td[4]/text()').extract()).strip()
            item['Low'] = Low
            
            Close = ''.join(itemPath.xpath('td[5]/text()').extract()).strip()
            item['Close'] = Close
            
            Volume = ''.join(itemPath.xpath('td[6]/span[1]/text()').extract()).strip()
            item['Volume'] = Volume
            
            yield item
