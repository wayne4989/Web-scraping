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
	# start_urls = (
	#     'http://www.ucc.org/find',
	# )
	   # https://uccwebservices.ucc.org/Mapping/FindAChurch.asmx/GetChurches
	def start_requests(self):
		headers = {
			# 'accept': "*/*",
			# 'accept-encoding': "gzip, deflate, br",
			# 'accept-language': "en-US,en;q=0.8",
			# 'connection': "keep-alive",
			# 'content-type': "application/json",
			# 'host': "api.dealroom.co",
			# 'origin': "https://app.tech.eu",
			# 'referer': "https://app.tech.eu/investors",
			# 'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
			# 'x-dealroom-app-id': "310816027",
			# 'x-requested-with': "XMLHttpRequest",
			# 'cache-control': "no-cache"

			'Accept': "application/json, text/javascript, */*; q=0.01",
			'Accept-Encoding': "gzip, deflate, br",
			'Accept-Language': "en-US,en;q=0.8",
			'Connection': "keep-alive",
			# Content-Length:122
			'Content-Type': "application/json; charset=UTF-8",
			# 'Cookie:__qca=P0-1713873674-1485367113500; ASP.NET_SessionId=n5i4y3vbf4bt2ognusetajde
			'Host': "uccwebservices.ucc.org",
			'Origin:https': "//uccwebservices.ucc.org",
			'Referer:https': "//uccwebservices.ucc.org/FindAChurch.aspx",
			'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
			'X-Requested-With': "XMLHttpRequest"
		}

		# {latitude: 40.62746865072138, longitude: -81.77075958251953, numchurches: 200, miles: 21.745142952617606, ONA_only: false}
		# for latitude_pos in range(24, 50):
		# 	for longitude_pos in range(-129, -65):
		for latitude_pos in self.seq(24, 50, 0.5):
			for longitude_pos in self.seq(-129, -65, 0.5):
				#print longitude_pos
				payload = "{latitude: %.2f, longitude: %.2f, numchurches: 200, miles: 43.17855066212449, ONA_only: false}" % (latitude_pos,longitude_pos)
				print payload
				url = "https://uccwebservices.ucc.org/Mapping/FindAChurch.asmx/GetChurches"
				yield scrapy.Request(url=url,method='POST',body=payload,callback=self.parse,headers=headers)

	def parse(self, response):

	    json_data = json.loads(response.body_as_unicode())
	    # self.logger.info( "-----------------------------" )
	    # self.logger.info( json_data )
	    item = UccscraperItem()
	    # {u'WEBSITE': u'http://www.nwoa.org/collegehill.htm', u'city': u'Bloomville ', u'Fax': None, u'Zip': u'44818-9348', u'address1': u'7632 State Rt 4 ', u'ONA': u'N', u'Contact': u'', u'ACCESS': u'Y', u'Phone': u'419-284-3744',
	     # u'state': u'OH', u'miles': u'6.3', u'CNNAME': u'College Hill UCC ', u'CONFCHU': u'520580', u'LATITUDE': u'40.980829', u'__type': u'UCCWebServices.Mapping.ChurchObject', u'Email': u'', u'LONGITUD': u'-82.929240'},
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
	        # item['Pasors'] = everychurch["CONFCHU"]
	        item['Email'] = everychurch["Email"]
	        item['Latitude'] = everychurch["LATITUDE"]
	        item['Logitude'] = everychurch["LONGITUD"]
	        item['Distance'] = everychurch["miles"]
	        yield item
	        
	def seq(self, start, end, step):
	    assert(step != 0)
	    sample_count = abs(end - start) / step
	    return itertools.islice(itertools.count(start, step), sample_count)
