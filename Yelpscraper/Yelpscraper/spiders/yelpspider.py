# -*- coding: utf-8 -*-
import scrapy
import proxylist
import useragent
from scrapy.http import Request
from Yelpscraper.items import YelpscraperItem
import requests
import time, re, random, base64
import json
from time import sleep

class YelpspiderSpider(scrapy.Spider):
    name = "yelpspider"
    allowed_domains = ["www.yelp.com"]
    start_urls = (
        'https://www.yelp.com/search?find_desc=Dermatologists&find_loc=US&start=0&cflt=dermatology',
    )
    proxy_lists = proxylist.proxys
    useragent_lists = useragent.user_agent_list

    def __init__(self) :
       
        self.base_url = 'https://www.yelp.com'
        self.url_header = 'http://'
        self.temp_num = 0  


    def set_proxies(self, url, callback):
        req = Request(url=url, callback=callback,dont_filter=True)
        proxy_url = self.proxy_lists[random.randrange(0,len(self.proxy_lists))]
        user_pass=base64.encodestring(b'user:password').strip().decode('utf-8')
        req.meta['proxy'] = "http://xxx.xxx.net:xxx"
        req.headers['Proxy-Authorization'] = 'Basic ' + user_pass
        user_agent = self.useragent_lists[random.randrange(0, len(self.useragent_lists))]
        req.headers['User-Agent'] = user_agent

        return req

    def parse(self, response):

        data_paths = response.xpath('//div[@class="search-results-content"]/ul[@class="ylist ylist-bordered search-results"]/li[@class="regular-search-result"]')
        for data_path in data_paths:
            text =  ' '.join(data_path.xpath('div[@class="search-result natural-search-result"]//span[@class="category-str-list"]/a/text()').extract()).strip()

            if("Dermatologists" in text):

                detail_url = data_path.xpath('div[@class="search-result natural-search-result"]//span[@class="indexed-biz-name"]/a/@href').extract()
                url = self.base_url + detail_url[0]

                req = self.set_proxies(url, self.parse_detail)

                title = data_path.xpath('div[@class="search-result natural-search-result"]/div[@class="biz-listing-large"]//div[@class="media-story"]/h3/span/a/span/text()').extract()
                address = ''.join(data_path.xpath('div[@class="search-result natural-search-result"]//div[@class="secondary-attributes"]/address/text()').extract()).strip()
                phone = ''.join(data_path.xpath('div[@class="search-result natural-search-result"]//div[@class="secondary-attributes"]/span[@class="biz-phone"]/text()').extract()).strip()
                req.meta['title'] = title
                req.meta['address'] = address
                req.meta['phone'] = phone

                sleep(5)
                yield req

        next_page = response.xpath('//div[@class="pagination-links arrange_unit"]//a[@class="u-decoration-none next pagination-links_anchor"]/@href').extract()
        if next_page > 0:
            url = self.base_url + next_page[0]

            req.meta['title'] = title
            req.meta['address'] = address
            req.meta['phone'] = phone

            req = self.set_proxies(url, self.parse)

            yield req

    def parse_detail(self, response):
        self.logger.info( "-----------------------------" )
        item = YelpscraperItem()

        title = response.meta['title']
        address = response.meta['address']
        phone = response.meta['phone']

      
        path = response.xpath('//span[@class="biz-website js-add-url-tagging"]')
        website = ''.join(path.xpath('a/text()').extract()).strip()
        website = website.replace("\%\E2\%\80\%\A6", "")
        website = website.replace("t\%\E2\%\80\%\A6", "")
        website = website.replace(".\%\E2\%\80\%\A6", "")

        if( len(website) == 0 ):

            item['Name'] = title
            item['Phone'] = phone
            item['Address'] = address
            yield item

        else:
            url = self.url_header + website
            req = self.set_proxies(url, self.parse_email)

            req.meta['title'] = title
            req.meta['address'] = address
            req.meta['phone'] = phone
            req.meta['website'] = website

            yield req

        item_url = ''.join(path.xpath('a/@href').extract()).strip()
        if item_url:
            pos  = re.search(r'url\=http%3A%2F%2F([\%\w\.]+)\&website\_link\_type\=', item_url, re.M|re.I|re.S)

            if pos:

                url = self.url_header + pos.group(1)        

                req = self.set_proxies(url, self.parse_email)

                req.meta['title'] = title
                req.meta['address'] = address
                req.meta['phone'] = phone
                req.meta['website'] = website

                yield req

    def parse_email(self, response):

        item = YelpscraperItem()
        title = response.meta['title']
        address = response.meta['address']
        phone = response.meta['phone']
        website = response.meta['website']

        emails = re.findall(r'[\w\.-]+@[\w\.-]+', response.body)
        self.logger.info( emails )
        if emails:
            emails = ''.join(emails[0]).strip()
            if(".png" in emails):
                emails = ""

        item['Name'] = title
        item['Phone'] = phone
        item['Address'] = address
        item['Email'] = emails
        item['Website'] = website

        yield item