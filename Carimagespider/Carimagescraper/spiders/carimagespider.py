# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
from copy import deepcopy
from time import sleep
from Carimagescraper.items import ImageItem
import time, re, random, base64, datetime
import csv, json
import numpy as np

class CarimagespiderSpider(scrapy.Spider):
    name = "carimagespider"
    allowed_domains = ["factorypreownedcollection.com"]
    start_urls = (
        'http://www.factorypreownedcollection.com/VehicleSearchResults',
    )

    def parse(self, response):

        with open('imgUrl1.csv', 'rb') as f:
            reader = csv.reader(f)
            items_list = list(reader)  
                  
        image_lists = np.array(items_list)
        image_item = ImageItem()
        image_item['image_urls'] = image_lists[:,0]
        yield image_item