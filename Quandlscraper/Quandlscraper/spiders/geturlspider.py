# -*- coding: utf-8 -*-
import scrapy
import useragent
from scrapy.http import Request, FormRequest
from Quandlscraper.items import QuandlurlItem
import time, datetime, csv, random, base64
import json

class GeturlspiderSpider(scrapy.Spider):
    name = "geturlspider"
    allowed_domains = ["quanddl.com"]

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

    base_url = "https://www.quandl.com/data/"

    def set_proxies(self, url, callback, headers=None):

        req = Request(url=url, callback=callback, dont_filter=True, headers= headers)
        user_pass=base64.encodestring(b'user:password').strip().decode('utf-8')
        req.meta['proxy'] = "http://xxx.xxx.net:xxx"
        req.headers['Proxy-Authorization'] = 'Basic ' + user_pass
        user_agent = self.useragent_lists[random.randrange(0, len(self.useragent_lists))]
        req.headers['User-Agent'] = user_agent

        return req

    def start_requests(self):
        self.logger.info("===== Start =====")
   
        # read varid from csv file
        for page in range(1,734):
            self.logger.info("----------------------")
            url = "https://www.quandl.com/api/v3/datasets?database_code=CFTC&include%5B%5D=latest_values&include%5B%5D=related_datasets&page=" + str(page) + "&per_page=20&query=commitment+of+traders+futures+only"
            self.logger.info(url)
            req = self.set_proxies(url, self.getPairID, self.headers)
            yield req  

    def getPairID(self, response):

        self.logger.info("===== Get ID =====")
        item = QuandlurlItem()
        json_data = json.loads(response.body)

        for every in json_data["datasets"]:
            database_code = every['database_code']
            dataset_code = every['dataset_code']
            urlize_name = every['urlize_name']
            url = self.base_url + database_code + "/" + dataset_code + "-" + urlize_name
            item['url'] = url

            ID = every['id']
            item['ID'] = ID
            yield item
            
