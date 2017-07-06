# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from Todscraper.items import TodscraperItem
import requests
import re
import json

class TodspiderSpider(scrapy.Spider):
    name = "todspider"
    allowed_domains = ["tods.com"]
    start_urls = (
        'http://www.tods.com/it_it/boutique/',
    )
    def __init__(self):

        self.temp_num = 0
        self.brand    = 'Tods'
    def parse(self, response):

        req_txt = requests.get(  url='http://www.geocms.it/Server/servlet/S3JXServletCall?parameters=method_name%3DGetObject%26callback%3Dscube.geocms.GeoResponse.execute%26id%3D5%26query%3D%26clear%3Dtrue%26licenza%3Dgeo-todsgroupspa%26progetto%3DTods%26lang%3Dit&encoding=UTF-8',
                       ).text
        store_list = req_txt.split('country')
        for store in store_list:

            self.temp_num = self.temp_num + 1

            if self.temp_num > 234 :

                return
            item = TodscraperItem()
            try:
            	if (self.temp_num > 1) :

                    pos = re.search(r'\\"address\\":\\"(.*?)".*\\"city\\":\\"(.*?)".*\\"name\\":\\"(.*?)".*\\"x\\":\\"(.*?)".*\\"y\\":\\"(.*?)"', store, re.M|re.I|re.S)
                    
                    item['Address']   = pos.group(1)
                    item['City']      = pos.group(2)
                    item['Name']      = pos.group(3)
                    item['Latitute']  = pos.group(4)
                    item['Longitude'] = pos.group(5)
                    item['Brand']     = "Tods"

                    phone_exc = re.search(r'\\"phone\\":\\"(.*?)"', store, re.M|re.I|re.S)
                    item['Shoptype']  = phone_exc.group(1)

            except:
                pass
            yield item
