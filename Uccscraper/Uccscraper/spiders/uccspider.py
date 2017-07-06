# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from Uccscraper.items import UccscraperItem
import requests
import re
import json
import itertools

class UccspiderSpider(scrapy.Spider):
	name = "uccspider"
	allowed_domains = ["ucc.org"]

	def start_requests(self):
		headers = {
			'Accept': "application/json, text/javascript, */*; q=0.01",
			'Accept-Encoding': "gzip, deflate, br",
			'Accept-Language': "en-US,en;q=0.8",
			'Connection': "keep-alive",
			'Content-Type': "application/json; charset=UTF-8",
			'Host': "uccwebservices.ucc.org",
			'Origin:https': "//uccwebservices.ucc.org",
			'Referer:https': "//uccwebservices.ucc.org/FindAChurch.aspx",
			'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
			'X-Requested-With': "XMLHttpRequest"
		}

		for latitude_pos in self.seq(24, 50, 0.5):
			for longitude_pos in self.seq(-129, -65, 0.5):
				payload = "{latitude: %.2f, longitude: %.2f, numchurches: 200, miles: 43.17855066212449, ONA_only: false}" % (latitude_pos,longitude_pos)
				print payload
				url = "https://uccwebservices.ucc.org/Mapping/FindAChurch.asmx/GetChurches"
				yield scrapy.Request(url=url,method='POST',body=payload,callback=self.parse,headers=headers)

	def parse(self, response):

	    json_data = json.loads(response.body_as_unicode())

	    item = UccscraperItem()
	    for everychurch in json_data["d"]:

	        item['Web'] = everychurch["WEBSITE"]
	        item['City'] = everychurch["city"]
	        item['Fax'] = everychurch["Fax"]
	        item['Zip'] = everychurch["Zip"]
	        item['Address'] = everychurch["address1"]
	        item['ONA'] = everychurch["ONA"]
	        item['Pasors'] = everychurch["Contact"]
	        item['Accessible'] = everychurch["ACCESS"]
	        item['Phone'] = everychurch["Phone"]
	        item['State'] = everychurch["state"]
	        item['Name_of_Church'] = everychurch["CNNAME"]
	        item['Email'] = everychurch["Email"]
	        item['Latitude'] = everychurch["LATITUDE"]
	        item['Logitude'] = everychurch["LONGITUD"]
	        item['Distance'] = everychurch["miles"]
	        yield item
	        
	def seq(self, start, end, step):
	    assert(step != 0)
	    sample_count = abs(end - start) / step
	    return itertools.islice(itertools.count(start, step), sample_count)
