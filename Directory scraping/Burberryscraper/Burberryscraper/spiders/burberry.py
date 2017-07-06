# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from Burberryscraper.items import BurberryscraperItem
import json
import requests

class BurberrySpider(scrapy.Spider):
    name = "burberry"
    allowed_domains = ["burberry.com"]
    start_urls = (
        'https://it.burberry.com/trovare-boutique/',
    )

    def __init__(self):

        self.temp_num = 0
        self.brand    = 'Burberry'
        self.url = "https://it.burberry.com/trovare-boutique/"

    def parse(self,response):
        country_list = [ "italia",
                         "austria", 
                         "belgio",
                         "repubblica-ceca",
                         "danimarca",
                         "emirati-arabi-uniti",
                         "estonia",
                         "finlandia",
                         "francia",
                         "germania",
                         "ungheria",
                         "irlanda",
                         "lettonia",
                         "lituania",
                         "olanda",
                         "norvegia",
                         "polonia",
                         "portogallo",
                         "romania",
                         "russia",
                         "spagna",
                         "svezia",
                         "svizzera",
                         "turchia",
                         "ucraina",
                         "regno-unito",
                         "brasile",
                         "canada",
                         "messico",
                         "stati-uniti-damerica",
                         "australia",
                         "cina",
                         "hong-kong",
                         "india",
                         "indonesia",
                         "giappone",
                         "macao",
                         "malesia",
                         "mongolia",
                         "filippine",
                         "singapore",
                         "korea-del-sud",
                         "taiwan",
                         "thailandia",
                         "vietnam",
                         "bahrein",
                         "egitto",
                         "giordania",
                         "kuwait",
                         "libano",
                         "qatar",
                         "arabia-saudita",
                         "armenia",
                         "azerbaijan",
                         "bahrein",
                         "croazia",
                         "georgia",
                         "kazakistan",
                         "sudafrica"
                         ]
        # print( response.url )
        for country in country_list:
            country_url = self.url + country

            req = Request(url=country_url, callback=self.country_detail, dont_filter=True)
            req.meta['country_name'] = country
            yield req

    def country_detail(self, response):

        cnt_name = response.meta['country_name']
        req_json = requests.get(  url='https://it.burberry.com/burberry/storeset/json/stores.jsp?country=' + cnt_name + '&__lang=it',
                              headers={ 'X-NewRelic-ID'   : 'XQMDVFdaGwQEV1FaAwc=',
                                        'X-Requested-With': 'XMLHttpRequest'} ).json()

        for store in req_json['stores']:

            item = BurberryscraperItem()  

            item['City'] = store['city']
            item['Name'] = store['name']
            address1 = store['address1']
            address2 = store['address2']
            address3 = store['address3']

            item['Address'] = address1 + address2 + address3
            item['Shoptype'] = store['phone']
            item['Latitute'] = store['coords']['lat']
            item['Longitude'] = store['coords']['lng']
            item['Brand'] = self.brand

            yield item
