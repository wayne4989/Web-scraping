# -*- coding: utf-8 -*-
import scrapy
import useragent
from scrapy.http import Request, FormRequest
from Ftscraper.items import SymbolsItem
import time, datetime, csv, random, base64, re, json
import sys
import MySQLdb
from scrapy.utils.project import get_project_settings


settings = get_project_settings()

dbargs = settings.get('DB_CONNECT')    
db_server = settings.get('DB_SERVER')    
db = MySQLdb.connect(dbargs['host'], dbargs['user'], dbargs['passwd'], dbargs['db'])
cursor = db.cursor()

class SymbolspiderSpider(scrapy.Spider):
    name = "symbolspider"
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
                    url = "https://markets.ft.com/data/equities/tearsheet/profile?s=" + Symb

                    req = self.set_proxies(url, self.getProfileData)

                    req.meta['secid'] = secid

                    yield req
      
                # return 

    def getProfileData(self, response):
        self.logger.info("====== Get Symb =======")
        item = SymbolsItem()

        secid = response.meta['secid']
        item['secid'] = secid

        symblists = response.xpath('//div[@class="mod-ui-symbol-chain"]//a[@class="mod-ui-link"]/@href').extract()
        for symblist in symblists:
            symb = symblist.split("=")[-1]

            symbol = symb.split(":")[0]
            item['Symbol'] = symbol

            market = symb.split(":")[1]
            item['Market'] = market

            yield item