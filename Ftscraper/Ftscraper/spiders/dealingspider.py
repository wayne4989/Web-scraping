# -*- coding: utf-8 -*-
import scrapy
import useragent
from scrapy.http import Request, FormRequest
from Ftscraper.items import DealingsItem
import time, datetime, csv, random, base64, re, json
import sys
import MySQLdb
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

dbargs = settings.get('DB_CONNECT')    
db_server = settings.get('DB_SERVER')    
db = MySQLdb.connect(dbargs['host'], dbargs['user'], dbargs['passwd'], dbargs['db'])
cursor = db.cursor()

class DealingspiderSpider(scrapy.Spider):
    name = "dealingspider"
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
                    url = "https://markets.ft.com/data/equities/tearsheet/directors?s=" + Symb
                    req = self.set_proxies(url, self.getParam)

                    req.meta['secid'] = secid
                    # req.meta['url'] = url

                    yield req
                # if listCount>3:
                #     return 

    def getParam(self, response):
        # self.logger.info("====== Get param =======")
        # c_url = response.meta['url']
        # print c_url
        secid = response.meta['secid']

        symbols = ''.join(response.xpath('//input[@name="symbols"]/@value').extract()).strip()
        url = "https://markets.ft.com/research/webservices/companies/v1/directordealings?officer=&position=&symbols=" + symbols + "&source=51d7791a57&limit=5&offset=0"
        req = self.set_proxies(url, self.getFirstData)

        req.meta['secid'] = secid
        req.meta['symbols'] = symbols

        yield req


    def getFirstData(self, response):
        # self.logger.info("====== getFirstData =======")
        secid = response.meta['secid']
        symbols = response.meta['symbols']

        item = DealingsItem()

        json_data = json.loads(response.body)

        totalNumber = json_data["data"]["items"][0]["directorTransactions"]["totalItems"]

        if totalNumber<5:
            item['secid'] = secid
            for itemdata in json_data["data"]["items"][0]["directorTransactions"]["items"]:
                try:
                    item['Date'] = itemdata["date"]
                except:
                    item['Date'] = ""

                try:
                    item['Type'] = itemdata["transType"]
                except:
                    item['Type'] = ""

                try:
                    item['Name'] = itemdata["officer"]
                except:
                    item['Nmae'] = ""

                try:
                    item['Title'] = itemdata["position"]
                except:
                    item['Title'] = ""

                try:
                    item['Shares'] = itemdata["numShares"]
                except:
                    item['Shares'] = ""

                try:
                    item['Pershare'] = itemdata["price"]
                except:
                    item['Pershare'] = ""

                try:
                    item['Dealsize'] = itemdata["totalValue"]
                except:
                    item['Dealsize'] = ""
                    
                yield item
        else:
            # print totalNumber
            # num = int(totalNumber)/5
            # mod = int(totalNumber)%5
            # print num
            # print mod
            for count in range(1, num+1):

                offset = count*5
                offset_str = str(count*5)
                url = "https://markets.ft.com/research/webservices/companies/v1/directordealings?officer=&position=&symbols=" + symbols + "&source=51d7791a57&limit=5&offset=" + offset_str
                req = self.set_proxies(url, self.getData)
                req.meta['secid'] = secid
                yield req

            last_offset = str(offset + mod)
            lastUrl = "https://markets.ft.com/research/webservices/companies/v1/directordealings?officer=&position=&symbols=" + symbols + "&source=51d7791a57&limit=5&offset=" + last_offset
            req = self.set_proxies(lastUrl, self.getData)
            req.meta['secid'] = secid
            yield req

    def getData(self, response):
        self.logger.info("====== getData =======")

        secid = response.meta['secid']

        item = DealingsItem()

        json_data = json.loads(response.body)
        item['secid'] = secid

        for itemdata in json_data["data"]["items"][0]["directorTransactions"]["items"]:
            try:
                item['Date'] = itemdata["date"]
            except:
                item['Date'] = ""

            try:
                item['Type'] = itemdata["transType"]
            except:
                item['Type'] = ""

            try:
                item['Name'] = itemdata["officer"]
            except:
                item['Nmae'] = ""

            try:
                item['Title'] = itemdata["position"]
            except:
                item['Title'] = ""

            try:
                item['Shares'] = itemdata["numShares"]
            except:
                item['Shares'] = ""

            try:
                item['Pershare'] = itemdata["price"]
            except:
                item['Pershare'] = ""

            try:
                item['Dealsize'] = itemdata["totalValue"]
            except:
                item['Dealsize'] = ""

            yield item        