# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from Skinscriptrxscraper.items import SkinscriptrxscraperItem
import requests
import json
import itertools

class SkinrxspiderSpider(scrapy.Spider):
	name = "skinrxspider"
	allowed_domains = ["skinscriptrx.com"]

	def start_requests(self):
		headers = {
			'X-Requested-With': "XMLHttpRequest"
		}

		for latitude_pos in self.seq(24, 50, 0.5):
			for longitude_pos in self.seq(-129, -65, 0.5):

				geo_str = "lat=%.2f&lng=%.2f" % (latitude_pos,longitude_pos)
				url = "http://www.skinscriptrx.com/?sm-xml-search=1&" + geo_str + "&radius=25&namequery=33.3684114%2C%20-111.9343636&query_type=all&limit=50&address&city&state&zip&pid=1783"
				yield scrapy.Request(url=url,method='GET',callback=self.parse,headers=headers)
	def parse(self, response):
		
		# http://www.skinscriptrx.com/?sm-xml-search=1&lat=33.368214&lng=-111.934146&radius=10&namequery=33.3684114%2C%20-111.9343636&query_type=all&limit=50&address&city&state&zip&pid=1783

		item = SkinscriptrxscraperItem()
		json_data = json.loads(response.body_as_unicode())
		# self.logger.info( "-----------------------------" )
		# self.logger.info( json_data ) 
		for everyskin in json_data:

			item['Name'] = everyskin["name"]
			item['Address1'] = everyskin["address"]
			item['Address2'] = everyskin["address2"]
			item['City'] = everyskin["city"]
			item['State'] = everyskin["state"]
			item['Zip'] = everyskin["zip"]
			item['Phone'] = everyskin["phone"]
			item['Email'] = everyskin["email"]
			item['Website'] = everyskin["url"]
			item['Lat'] = everyskin["lat"]
			item['Lng'] = everyskin["lng"]

			yield item



	def seq(self, start, end, step):
		assert(step != 0)
		sample_count = abs(end - start) / step
		return itertools.islice(itertools.count(start, step), sample_count)