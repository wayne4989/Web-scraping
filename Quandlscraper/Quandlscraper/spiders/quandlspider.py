# -*- coding: utf-8 -*-
import scrapy
import useragent
from scrapy.http import Request, FormRequest
from Quandlscraper.items import QuandlscraperItem
import time, datetime, csv, random, base64
import json

class QuandlspiderSpider(scrapy.Spider):

    name = "quandlspider"
    allowed_domains = ["quandl.com"]
    select_param = ""
    useragent_lists = useragent.user_agent_list

    headers = {
        'accept':'application/json, application/vnd.quandl+json',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'en-GB,en-US;q=0.8,en;q=0.6',
        'request-source':'next',
        'request-version':'3.5.0+5df0510b',
        'x-api-token':'bCqxQUARAjNBsqZHj4yb',
        'x-requested-with':'XMLHttpRequest',        
    }

    def __init__(self,  param ='', *args, **kwargs):

        super(QuandlspiderSpider, self).__init__(*args, **kwargs)
        
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

        if (self.select_param.isdigit()!=True and self.select_param!="all"):
            print("===== Please Insert Correct Command!!! =====")
            print("* Case Get All Data : scrapy crawl quandlspider -a param=all")
            print("* Case Get n Columns : scrapy crawl quandlspider -a param=n (ex: If you want to get 6 columns, param=6)")

            return

        with open('url_list.csv') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:

                log_url = ''.join(row['url']).strip()
                ID = ''.join(row['ID']).strip()

                url = "https://www.quandl.com/api/v3/datasets/" + str(ID) + "/data"
                req = self.set_proxies(url, self.getData, self.headers)
                req.meta['log_url'] = log_url
                req.meta['ID'] = ID

                yield req

    def getData(self, response):
        self.logger.info("=========== Get Api-Tocken ==========")

        json_data = json.loads(response.body)

        ID = response.meta['ID']
        log_url = response.meta['log_url']

        column_names = []
        data_buf = []

        item = QuandlscraperItem()

        item['ID'] = ID

        if "dataset_data" in json_data:

            for column_name in json_data["dataset_data"]["column_names"]:

                column_names.append(column_name)

            if self.select_param=="all":

                for every in json_data["dataset_data"]["data"]:

                    item['Date'] = every[0]                

                    for coun, column_name in enumerate(column_names):
                        if coun==0:
                            continue

                        data = column_name + " : " + str(int(every[coun]))
                        data_buf.append(data)
                        
                    item['Data'] = str(', '.join(data_buf).strip())

                    yield item

                    del data_buf[:]


                log_txt = log_url + ", param=" + str(self.select_param)
                self.makeLog(log_txt)

            else:

                count = 1

                for every in json_data["dataset_data"]["data"]:

                    item['Date'] = every[0]                

                    for coun, column_name in enumerate(column_names):
                        if coun==0:
                            continue

                        data = column_name + " : " + str(int(every[coun]))
                        data_buf.append(data)
                        
                    item['Data'] = str(', '.join(data_buf).strip())

                    yield item

                    del data_buf[:]

                    count = count + 1
                    if count > int(self.select_param):
                        log_txt = log_url + ", param=" + str(self.select_param)      
                        self.makeLog(log_txt)
                        return
        else:

            log_txt = log_url + ", error = 'There is no dataset_data in json file'"
            self.makeLog(log_txt)


    def makeLog(self, txt):

        standartdate = datetime.datetime.now()
        date = standartdate.strftime('%Y-%m-%d %H:%M:%S')
        fout = open("log.txt", "a")
        fout.write(str(date) + " -> " + txt + "\n")
        fout.close()

    def clearLog(self):
        fout = open("log.txt", "w")
        fout.close()