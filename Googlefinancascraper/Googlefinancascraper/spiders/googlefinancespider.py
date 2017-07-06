# -*- coding: utf-8 -*-
import scrapy
import useragent
from scrapy.http import Request, FormRequest
from Googlefinancascraper.items import GooglefinancascraperItem
import time, datetime, csv, random, base64, re
from datetime import datetime, timedelta
from time import sleep


class GooglefinancespiderSpider(scrapy.Spider):

    name = "googlefinancespider"
    allowed_domains = ["www.google.com"]
    select_param = ""
    useragent_lists = useragent.user_agent_list
    next_flag = True
    def __init__(self,  param = None, *args, **kwargs):

        super(GooglefinancespiderSpider, self).__init__(*args, **kwargs)
        
        self.select_param = param

    def set_proxies(self, url, callback):

        req = Request(url=url, callback=callback, dont_filter=True)
        user_pass=base64.encodestring(b'user:password').strip().decode('utf-8')
        req.meta['proxy'] = "http://xxx.xxx.net:xxx"
        req.headers['Proxy-Authorization'] = 'Basic ' + user_pass
        user_agent = self.useragent_lists[random.randrange(0, len(self.useragent_lists))]
        req.headers['User-Agent'] = user_agent

        return req

    def start_requests(self):

        self.clearLog()
        self.makeLog("=================== Start ===================")

        if (self.select_param!="all" and self.select_param.isdigit()!=True):
            print("===== Please Insert Correct Command!!! =====")
            print("* Case Get All Data : scrapy crawl googlefinancespider -a param=all")
            print("* Case Get Last x days : scrapy crawl googlefinancespider -a param=x (ex : param=3)")

            return

        myfile = open("url_list.csv", "rb")
        urllist = csv.reader(myfile)

        for i, url in enumerate(urllist):
            url=''.join(url).strip()
            req = self.set_proxies(url, self.getCid)
            req.meta['number'] = i+1
            req.meta['baseUrl'] = url

            yield req  

    def getCid(self, response):
        self.logger.info("============= Get Cid ===============")

        number = response.meta['number']
        baseUrl = response.meta['baseUrl']

        if self.select_param == "all":    
            self.logger.info("--------------- get all data -----------------")

            c = datetime.now()
            currentDate =  "%s+%s+%s" % (c.month, c.day, c.year)

            cid = ''.join(response.xpath('//input[@name="cid"]/@value').extract()).strip()

            url = "https://www.google.com/finance/historical?cid=%s&startdate=Jan+1+2000&enddate=%s&num=30" %(cid, currentDate)

            req = self.set_proxies(url, self.getData)

            req.meta['main_url'] = url
            req.meta['count'] = 30
            req.meta['number'] = number
            req.meta['baseUrl'] = baseUrl

            yield req

        else:
            self.logger.info("--------------- get last data -----------------")

            s = datetime.now() - timedelta(days=int(self.select_param))
            startdate = "%s+%s+%s" % (s.month, s.day, s.year)

            c = datetime.now()
            currentDate =  "%s+%s+%s" % (c.month, c.day, c.year)

            cid = ''.join(response.xpath('//input[@name="cid"]/@value').extract()).strip()

            url = "https://www.google.com/finance/historical?cid=%s&startdate=%s&enddate=%s&num=30" %(cid, startdate, currentDate)

            req = self.set_proxies(url, self.getData)

            req.meta['main_url'] = url
            req.meta['count'] = 30
            req.meta['number'] = number
            req.meta['baseUrl'] = baseUrl

            yield req

    def getData(self, response):
        self.logger.info("========= Get Data =========")

        item = GooglefinancascraperItem()
        url = response.meta['main_url']
        count = response.meta['count']
        number = response.meta['number']
        baseUrl = response.meta['baseUrl']

        dataPaths = response.xpath('//table[@class="gf-table historical_price"]/tr')
        if len(dataPaths)==0:
            
            log_txt = baseUrl + ", param=" + str(self.select_param)      
            self.makeLog(log_txt)            
            return

        for i, dataPath in enumerate(dataPaths):

            if i == 0:
                continue

            item['Number'] = number

            Date = ''.join(dataPath.xpath('td[1]/text()').extract()).strip()
            item['Date'] = Date

            Open = ''.join(dataPath.xpath('td[2]/text()').extract()).strip()
            item['Open'] = Open

            High = ''.join(dataPath.xpath('td[3]/text()').extract()).strip()
            item['High'] = High

            Low = ''.join(dataPath.xpath('td[4]/text()').extract()).strip()
            item['Low'] = Low

            Close = ''.join(dataPath.xpath('td[5]/text()').extract()).strip()
            item['Close'] = Close

            Volume = ''.join(dataPath.xpath('td[6]/text()').extract()).strip()
            item['Volume'] = Volume

            yield item

        next_url = url + "&start=%s" %count
        print number, count
        req = self.set_proxies(next_url, self.getData)
        count = count + 30

        req.meta['count'] = count
        req.meta['main_url'] = url
        req.meta['number'] = number
        req.meta['baseUrl'] = baseUrl

        yield req

    def makeLog(self, txt):

        standartdate = datetime.now()
        date = standartdate.strftime('%Y-%m-%d %H:%M:%S')
        fout = open("log.txt", "a")
        fout.write(str(date) + " -> " + txt + "\n")
        fout.close()

    def clearLog(self):
        fout = open("log.txt", "w")
        fout.close()
