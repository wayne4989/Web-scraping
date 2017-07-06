# -*- coding: utf-8 -*-
import scrapy
import useragent
from scrapy.http import Request, FormRequest
from Ieconomics.items import DataItem
from Ieconomics.items import ChartItem
import time, datetime, csv, random, base64, re, json

class IeconomicspiderSpider(scrapy.Spider):
    name = "ieconomicspider"
    allowed_domains = ["ieconomics.com"]
    select_param = ""
    useragent_lists = useragent.user_agent_list
    ChartID = 1

    def __init__(self,  param =None, *args, **kwargs):

        super(IeconomicspiderSpider, self).__init__(*args, **kwargs)
        
        self.select_param = param

    def set_proxies(self, url, callback, headers=None):

        req = Request(url=url, callback=callback, dont_filter=True, headers= headers)
        user_pass=base64.encodestring(b'user:password').strip().decode('utf-8')
        req.meta['proxy'] = "http://xxx.xxx.net:xxx"
        req.headers['Proxy-Authorization'] = 'Basic ' + user_pass
        user_agent = self.useragent_lists[random.randrange(0, len(self.useragent_lists))]
        req.headers['User-Agent'] = user_agent

        return req

    def start_requests(self):

        self.clearLog()
        self.makeLog("=================== Start ===================")

        with open('lists.csv') as csvfile:
            reader = csv.DictReader(csvfile)

            for listCount, row in enumerate(reader):

                country = ''.join(row['country']).strip()
                variable = ''.join(row['variable']).strip()

                url = "https://ieconomics.com/" + country + " " + variable
                req = self.set_proxies(url, self.getParam)

                req.meta['variableID'] = listCount + 1

                yield req  

    def getParam(self, response):
        self.logger.info("============= getParam ===============")

        headers = {
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en-US,en;q=0.8',
            'Content-Type':'application/json; charset=UTF-8',
        }
        variableID = response.meta['variableID']

        params = response.xpath('//span[@class="grid click-baiter onecolumn"]/@data-iids').extract()
        if len(params)==0:

            params = ''.join(response.xpath('//span[@class="grid click-baiter twocolumns"]/@data-iids').extract()).strip()
            for count, param in enumerate(params):

                url = "https://markets.tradingeconomics.com/econ/?s=" + param + "&span=max&lang=en&forecast=true&_=1498832549305"
                req = self.set_proxies(url, self.getData, headers=headers)

                req.meta['chart_Num'] = count + 1
                req.meta['variableID'] = variableID

                yield req
          
            return

        for count, param in enumerate(params):

            url = "https://markets.tradingeconomics.com/econ/?s=" + param + "&span=max&lang=en&forecast=true&_=1498832549305"
            req = self.set_proxies(url, self.getData, headers=headers)

            req.meta['chart_Num'] = count + 1
            req.meta['variableID'] = variableID

            yield req

    def getData(self, response):
        self.logger.info("============= getData ===============")

        item = ChartItem()

        variableID = response.meta['variableID']
        chart_Num = response.meta['chart_Num']
        item['VariableID'] = variableID
        item['ChartID'] = chart_Num
        json_data = json.loads(response.body)
        category = json_data[0]["series"][0]["serie"]["category"]
        item['Chartname'] = category

        yield item

        item = DataItem()
        item['chartID'] = self.ChartID
        for every in json_data[0]["series"][0]["serie"]["data"]:
            item['date' ] = every["date"]
            item['value'] = every["close"]

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