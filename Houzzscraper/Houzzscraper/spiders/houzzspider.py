# -*- coding: utf-8 -*-
import scrapy
import re
import proxylist
import useragent
from scrapy.http import Request, FormRequest
from Houzzscraper.items import HouzzscraperItem
import requests
import time, re, random, base64
import csv
import sys

class HouzzspiderSpider(scrapy.Spider):
    name = "houzzspider"
    allowed_domains = ["houzz.com"]
    start_urls = (
        'http://www.houzz.com/professionals/architect/s/Architects-%26-Building-Designers/c/Unionville%2C-CT',
    )
    proxy_lists = proxylist.proxys
    useragent_lists = useragent.user_agent_list
    count = 0


    def set_proxies(self, url, callback):

        header = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'en-US,en;q=0.8',
            'Connection':'keep-alive',
            'Host':'www.houzz.com',
            'Referer':'http://www.houzz.com/professionals/architect/s/Architects-%26-Building-Designers/c/Unionville%2C-CT',
            'Upgrade-Insecure-Requests':'1',
            }

        req = Request(url=url, callback=callback,dont_filter=True, headers= header)
        proxy_url = self.proxy_lists[random.randrange(0,len(self.proxy_lists))]
        user_pass=base64.encodestring(b'user:password').strip().decode('utf-8')
        req.meta['proxy'] = "http://xxx.xxx.net:xxx"
        req.headers['Proxy-Authorization'] = 'Basic ' + user_pass
        user_agent = self.useragent_lists[random.randrange(0, len(self.useragent_lists))]
        req.headers['User-Agent'] = user_agent

        return req

    def parse(self, response):
        self.logger.info("============== Start!!! ===============")
        
        paths = response.xpath('//div[@class="proDirectory withWizard"]//div[@class="pro-cover-photos"]')
        for path in paths:
            url = path.xpath('a/@href').extract()[0]
            self.logger.info(url)
            req = self.set_proxies(url, self.parse_data)
            yield req

        self.count = self.count + 1
        if(self.count > 3):
            return
        next_page = response.xpath('//div[@class="pagination-wrapper"]//a[@class="navigation-button next"]/@href').extract()
        if next_page:
            req = self.set_proxies(next_page[0], self.parse)
            yield req


    def parse_data(self, response):

        item = HouzzscraperItem()

        self.logger.info("-------------- stage1 ------------")

        profile = ''.join(response.xpath('//div[@class="profile-about-right"]/div[@class="text-bold"]/text()').extract()).strip()
        item['Profile'] = profile

        title = ''.join(response.xpath('//div[@class="profile-title"]/h1/a/text()').extract()).strip()
        item['Name'] = title

        phone = ''.join(response.xpath('//div[@class="pro-contact-methods one-line trackMe"]/span[@class="pro-contact-text"]/text()').extract()).strip()
        item['Phone'] = phone

        data1 = response.xpath('//div[@class="pro-info-horizontal-list text-m text-dt-s"]//i[@class="hzi-font hzi-Ruler"]')
        professional = ''.join(data1.xpath('following-sibling::div/span[@itemprop="child"]/a/span/text()').extract()).strip()
        item['Profession'] = professional

        data1 = response.xpath('//div[@class="pro-info-horizontal-list text-m text-dt-s"]//i[@class="hzi-font hzi-Man-Outline"]')
        contact = ''.join(data1.xpath('following-sibling::div/text()').extract()).strip()
        contact = contact.replace(": ", "")
        item['Contact'] = contact

        data1 = response.xpath('//div[@class="pro-info-horizontal-list text-m text-dt-s"]//i[@class="hzi-font hzi-Location"]')
        streetAddress = ''.join(data1.xpath('following-sibling::div/span[@itemprop="streetAddress"]/text()').extract()).strip()
        addressLocality = ''.join(data1.xpath('following-sibling::div/span[@itemprop="addressLocality"]/a/text()').extract()).strip()
        addressRegion = ''.join(data1.xpath('following-sibling::div/span[@itemprop="addressRegion"]/text()').extract()).strip()
        postalCode = ''.join(data1.xpath('following-sibling::div/span[@itemprop="postalCode"]/text()').extract()).strip()
        addressCountry = ''.join(data1.xpath('following-sibling::div/span[@itemprop="addressCountry"]/text()').extract()).strip()

        address = streetAddress + ", " + addressLocality + ", " + addressRegion + ", " +  postalCode + ", " +  addressCountry
        item['Location'] = address

        data1 = response.xpath('//div[@class="pro-info-horizontal-list text-m text-dt-s"]//i[@class="hzi-font hzi-License"]')
        license = ''.join(data1.xpath('following-sibling::div/text()').extract()).strip()
        license = license.replace(": ", "")
        item['License'] = license

        data1 = response.xpath('//div[@class="pro-info-horizontal-list text-m text-dt-s"]//i[@class="hzi-font hzi-Cost-Estimate"]')
        price = ''.join(data1.xpath('following-sibling::div/text()').extract()).strip()
        price = price.replace(": ", "")
        item['Price'] = price

        yield item