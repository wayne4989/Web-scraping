# -*- coding: utf-8 -*-
import scrapy
import useragent
from scrapy.http import Request, FormRequest
from Financescraper.items import FinancescraperItem
import time, datetime, csv, random, base64

class FinancespiderSpider(scrapy.Spider):
    name = "financespider"
    allowed_domains = ["finance.yahoo.com"]

    select_param = ""
    useragent_lists = useragent.user_agent_list

    def __init__(self,  param ='', *args, **kwargs):

        super(FinancespiderSpider, self).__init__(*args, **kwargs)
        
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
            print("* Case Get All Data : scrapy crawl financespider -a param=all")
            print("* Case Get n Columns : scrapy crawl financespider -a param=n (ex: If you want to get 6 columns, param=6)")

            return
        # ipUrl = 'http://lumtest.com/myip.json'
        # proxy_ip_req = self.set_proxies(ipUrl, self.get_proxy_ip)
        # yield proxy_ip_req
        # return

        myfile = open("url_list.csv", "rb")
        urllist = csv.reader(myfile)

        for i, url in enumerate(urllist):

            url=''.join(url).strip()
            req = self.set_proxies(url, self.getData)
            req.meta['number'] = i+1
            req.meta['url'] = url

            yield req  
            # return

    def getData(self, response):
        self.logger.info("============= Data Parse ===============")

        number = response.meta['number']
        url = response.meta['url']

        item = FinancescraperItem()

        dataPaths = response.xpath('//table[@data-test="historical-prices"]/tbody/tr')

        if(self.select_param == "all"):

            for row, dataPath in enumerate(dataPaths):

                if row==0:
                    continue

                text = ''.join(dataPath.xpath('td[2]/span/text()').extract()).strip()
                if text=="Dividend":

                    item['Number'] = number
                    
                    Date = ''.join(dataPath.xpath('td[1]/span/text()').extract()).strip()                 
                    item['Date'] = Date

                    Dividend = ''.join(dataPath.xpath('td[2]/strong/text()').extract()).strip()
                    item['Dividend'] = Dividend

                    item['Open'] = ""

                    item['High'] = ""

                    item['Low'] = ""

                    item['Close'] = ""

                    item['Adj_Close'] = ""

                    item['Volume'] = ""

                else:

                    item['Number'] = number
                    
                    Date = ''.join(dataPath.xpath('td[1]/span/text()').extract()).strip()
                    item['Date'] = Date

                    item['Dividend'] = "0"

                    Open = ''.join(dataPath.xpath('td[2]/span/text()').extract()).strip()
                    item['Open'] = Open

                    High = ''.join(dataPath.xpath('td[3]/span/text()').extract()).strip()
                    item['High'] = High

                    Low = ''.join(dataPath.xpath('td[4]/span/text()').extract()).strip()
                    item['Low'] = Low

                    Close = ''.join(dataPath.xpath('td[5]/span/text()').extract()).strip()
                    item['Close'] = Close

                    Adj_Close = ''.join(dataPath.xpath('td[6]/span/text()').extract()).strip()
                    item['Adj_Close'] = Adj_Close

                    Volume = ''.join(dataPath.xpath('td[7]/span/text()').extract()).strip()
                    item['Volume'] = Volume

                yield item  
                  
            log_txt = url + ", param=" + str(self.select_param)      
            self.makeLog(log_txt)

        else:

            count = 0

            for row, dataPath in enumerate(dataPaths):
                if row==0:
                    continue

                text = ''.join(dataPath.xpath('td[2]/span/text()').extract()).strip()
                if text=="Dividend":
 
                    item['Number'] = number
                    
                    Date = ''.join(dataPath.xpath('td[1]/span/text()').extract()).strip()                 
                    item['Date'] = Date

                    Dividend = ''.join(dataPath.xpath('td[2]/strong/text()').extract()).strip()
                    item['Dividend'] = Dividend

                    item['Open'] = ""

                    item['High'] = ""

                    item['Low'] = ""

                    item['Close'] = ""

                    item['Adj_Close'] = ""

                    item['Volume'] = ""

                else:

                    item['Number'] = number
                    
                    Date = ''.join(dataPath.xpath('td[1]/span/text()').extract()).strip()
                    item['Date'] = Date

                    item['Dividend'] = "0"

                    Open = ''.join(dataPath.xpath('td[2]/span/text()').extract()).strip()
                    item['Open'] = Open

                    High = ''.join(dataPath.xpath('td[3]/span/text()').extract()).strip()
                    item['High'] = High

                    Low = ''.join(dataPath.xpath('td[4]/span/text()').extract()).strip()
                    item['Low'] = Low

                    Close = ''.join(dataPath.xpath('td[5]/span/text()').extract()).strip()
                    item['Close'] = Close

                    Adj_Close = ''.join(dataPath.xpath('td[6]/span/text()').extract()).strip()
                    item['Adj_Close'] = Adj_Close

                    Volume = ''.join(dataPath.xpath('td[7]/span/text()').extract()).strip()
                    item['Volume'] = Volume

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

    #             self.logger.info(Date)
    #             self.logger.info(Open)
    #             self.logger.info(High)
    #             self.logger.info(Low)
    #             self.logger.info(Close)
    #             self.logger.info(Adj_Close)
    #             self.logger.info(Volume)

    # def get_proxy_ip(self, response):
    #     print response.body

