# -*- coding: utf-8 -*-
import scrapy
import useragent
from scrapy.http import Request, FormRequest
from Investscraper.items import InvestscraperItem
import time, datetime, csv, random, base64
import logging

class InvestspiderSpider(scrapy.Spider):
    name = "investspider"
    allowed_domains = ["investing.com"]

    url = "https://www.investing.com/equities/3m-co-historical-data"

    select_param = ""
    useragent_lists = useragent.user_agent_list

    def __init__(self,  param ='', *args, **kwargs):

        super(InvestspiderSpider, self).__init__(*args, **kwargs)
        
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

        if (self.select_param.isdigit()!=True and self.select_param!="all"):
            print("===== Please Insert Correct Command!!! =====")
            print("* Case Get All Data : scrapy crawl investspider -a param=all")
            print("* Case Get n Columns : scrapy crawl investspider -a param=n (ex: If you want to get 6 columns, param=6)")

            return

        myfile = open("url_list.csv", "rb")
        urllist = csv.reader(myfile)

        for url in urllist:

            url=''.join(url).strip()
            req = self.set_proxies(url, self.getCurrId)
            req.meta['url'] = url

            yield req      

    def getCurrId(self, response):
        self.logger.info("============= Get CurrId ===============")
        url = response.meta['url']

        headers = {        
            'Content-Type':'application/x-www-form-urlencoded',
            'X-Requested-With':'XMLHttpRequest',
        }

        i = datetime.datetime.now()
        currentDate =  "%s/%s/%s" % (i.month, i.day, i.year)

        currId = ''.join(response.xpath('//div[@class="headBtnWrapper float_lang_base_2 js-add-to-portfolio"]/@data-pair-id').extract()).strip()

        req = scrapy.FormRequest(
        
            url="https://www.investing.com/instruments/HistoricalDataAjax",
            formdata={
                'action':'historical_data',
                'curr_id': currId,
                'st_date': '01/01/2000',
                'end_date': currentDate,
                'interval_sec':'Daily'
            },
            headers=headers,
            callback=self.getData
        )

        req.meta['currId'] = currId
        req.meta['url'] = url

        yield req

    def getData(self, response):
        self.logger.info("============= Data Parse ===============")


        item = InvestscraperItem()

        currId = response.meta['currId']
        url = response.meta['url']

        item['Curr_Id'] = currId

        dataPaths = response.xpath('//table[@id="curr_table"]/tbody/tr')

        if(self.select_param == "all"):

            for row, dataPath in enumerate(dataPaths):

                if row==0:
                    continue
                
                Date = ''.join(dataPath.xpath('td[1]/text()').extract()).strip()
                item['Date'] = Date

                Price = ''.join(dataPath.xpath('td[2]/text()').extract()).strip()
                item['Price'] = Price

                Open = ''.join(dataPath.xpath('td[3]/text()').extract()).strip()
                item['Open'] = Open

                High = ''.join(dataPath.xpath('td[4]/text()').extract()).strip()
                item['High'] = High

                Low = ''.join(dataPath.xpath('td[5]/text()').extract()).strip()
                item['Low'] = Low

                Vol = ''.join(dataPath.xpath('td[6]/text()').extract()).strip()
                item['Vol'] = Vol

                yield item

            log_txt = url + ", param=" + str(self.select_param)      
            self.makeLog(log_txt)

        else:

            count = 0

            for row, dataPath in enumerate(dataPaths):
                
                if row==0:
                    continue
                
                Date = ''.join(dataPath.xpath('td[1]/text()').extract()).strip()
                item['Date'] = Date

                Price = ''.join(dataPath.xpath('td[2]/text()').extract()).strip()
                item['Price'] = Price

                Open = ''.join(dataPath.xpath('td[3]/text()').extract()).strip()
                item['Open'] = Open

                High = ''.join(dataPath.xpath('td[4]/text()').extract()).strip()
                item['High'] = High

                Low = ''.join(dataPath.xpath('td[5]/text()').extract()).strip()
                item['Low'] = Low

                Vol = ''.join(dataPath.xpath('td[6]/text()').extract()).strip()
                item['Vol'] = Vol

                count = count + 1
                if count > int(self.select_param):
                    log_txt = url + ", param=" + str(self.select_param)      
                    self.makeLog(log_txt)
                    return

                yield item

    def makeLog(self, txt):

        standartdate = datetime.datetime.now()
        date = standartdate.strftime('%Y-%m-%d %H:%M:%S')
        fout = open("log.txt", "a")
        fout.write(str(date) + " -> " + txt + "\n")
        fout.close()

    def clearLog(self):
        fout = open("log.txt", "w")
        fout.close()