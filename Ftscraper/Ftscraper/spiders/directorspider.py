# -*- coding: utf-8 -*-
import scrapy
import useragent
from scrapy.http import Request, FormRequest
from Ftscraper.items import DirectorsItem
import time, datetime, csv, random, base64, re, json
import sys
import MySQLdb
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

dbargs = settings.get('DB_CONNECT')    
db_server = settings.get('DB_SERVER')    
db = MySQLdb.connect(dbargs['host'], dbargs['user'], dbargs['passwd'], dbargs['db'])
cursor = db.cursor()

class DirectorspiderSpider(scrapy.Spider):
    name = "directorspider"
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
                    req = self.set_proxies(url, self.getDirectorsData)

                    req.meta['secid'] = secid

                    yield req
      
                # return 

    def getDirectorsData(self, response):
        self.logger.info("====== Get directors =======")
        item = DirectorsItem()

        secid = response.meta['secid']
        item['secid'] = secid

        itemPaths = response.xpath('//table[@class="mod-ui-table mod-ui-table--freeze-pane"]/tbody/tr')
        # self.logger.info(len(itemPaths))
        for itemPath in itemPaths:
            # self.logger.info("--------------------------")

            Name = ''.join(itemPath.xpath('td[1]/text()').extract()).strip()
            item['Name'] = Name
            # self.logger.info(Name)

            Title = ''.join(itemPath.xpath('td[2]/text()').extract()).strip()
            item['Title'] = Title
            # self.logger.info(Title)

            Compensation = ''.join(itemPath.xpath('td[3]/span/text()').extract()).strip()
            item['Compensation'] = Compensation
            # self.logger.info(Compensation)

            Age = ''.join(itemPath.xpath('td[4]/text()').extract()).strip()
            item['Age'] = Age
            # self.logger.info(Age)            

            Officer_since = ''.join(itemPath.xpath('td[5]/text()').extract()).strip()
            item['Since'] = Officer_since
            # self.logger.info(Officer_since)  
            yield item 