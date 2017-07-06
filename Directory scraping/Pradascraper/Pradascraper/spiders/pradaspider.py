# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from Pradascraper.items import PradascraperItem
import requests
import re

class PradaspiderSpider(scrapy.Spider):
    name = "pradaspider"
    allowed_domains = ["prada.com"]
    start_urls = (
        'http://www.prada.com/en/store-locator.html',
    )

    def parse(self, response):

        res_map = requests.get(  url='http://www.prada.com/en/store-locator/jcr:content/storelocator/storelocator.content.html?288&lat=0&lng=0&zoom=0&nord=40.17887331434696&sud=-40.17887331434695&est=64.6875&ovest=-64.6875&category=',
                             headers={ 'X-Requested-With': 'XMLHttpRequest'} )
        store_list = res_map.text.split('s={};')
        for store in store_list:
            try:
                item = PradascraperItem()
                pos  = re.search(r's.latitude=([\-\.0-9]+); s.longitude=([\-\.0-9]+).*s.title="(.*?)";.*s.addressHTML="(.*?)";.*s.phone="(.*?)";', store, re.M|re.I|re.S)
                item['Latitute']  = pos.group(1)
                item['Longitude'] = pos.group(2)
                item['Name'] = pos.group(3)
                address      = pos.group(4)
                address_txt  = address.replace("<br />","")
                item['Address']  = address_txt
                shoptype         = pos.group(5)
                shoptype_txt     = shoptype.replace("<br />","")
                item['Shoptype'] = shoptype_txt
                item['Brand']    = "Prada"

            except:
                pass
            yield item
