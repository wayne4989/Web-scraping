# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from streetscraper.items import StreetscraperItem
import re
import requests

class StreetspiderSpider(scrapy.Spider):
    name = "streetspider"
    allowed_domains = ["street.com"]
    start_urls = (
        'http://streeteasy.com/for-sale/nyc',
    )

    def __init__(self):

        self.temp_num = 0

    def parse(self, response):

        for apart_featured in response.xpath('//div[@class="item featured"]') :
            apart_url = response.urljoin(apart_featured.xpath('div[@class="photo"]/a/@href')[0].extract())
            req = Request(url=apart_url, callback=self.apart_detail, dont_filter=True)
            req.meta['url'] = apart_url
            yield req

        for apart in response.xpath('//div[@class="item"]') :
            apart_url = response.urljoin(apart.xpath('div[@class="photo"]/a/@href')[0].extract())
            req = Request(url=apart_url, callback=self.apart_detail, dont_filter=True)
            req.meta['url'] = apart_url
            yield req

        next_page = response.xpath('//div[@class="pagination center_aligned bottom_pagination big_space"]/nav/span[@class="next"]/a/@href').extract()

        if ( len(next_page) == 1 ) :

            yield Request(url='http://streeteasy.com' + next_page[0], callback=self.parse, dont_filter=True)

    def apart_detail(self, response):

        info_url = response.xpath('//div[@class="right-two-fifths"]/div[@class="main-info"]')
        item = StreetscraperItem()

        item['URL'] = response.meta['url']

        address = ' '.join(info_url.xpath('h1/a/text()').extract()).strip()
        if( len(address)>0 ):
            item['Address'] = address

        price = ' '.join(info_url.xpath('div[@class="details"]/div[@class="details_info_price"]/div/text()').extract()).strip()
        item['Price'] = price

        nofee = ' '.join(info_url.xpath('div[@class="details"]/div[@class="details_info_price"]/div[@class="status nofee"]/a/text()').extract()).strip()
        if (len(nofee) == 0):
            item['NO_FEE'] = "False"
        if (len(nofee) > 0):
            item['NO_FEE'] = "True"

        location = ' '.join(info_url.xpath('div[@class="details"]/div[@class="details_info"]/span[@class="nobreak"]/a/text()').extract()).strip()
        item['Location'] = location


        square = ' '.join(info_url.xpath('div[@class="details"]/div[@class="details_info"]/span[contains(@class, "detail_cell") and contains(text(), "ft") and not(contains(text(), "per"))]/text()').extract()).strip()

        if( len(square)>0 ):
            sqft = re.search(r'[0-9/,]*', square)
            item['Sqft'] = sqft.group(0)

        rooms = ' '.join(info_url.xpath('div[@class="details"]/div[@class="details_info"]/span[contains(@class, "detail_cell") and contains(text(), "room")]/text()').extract()).strip()

        if( len(rooms)>0 ):
            room = re.search(r'[0-9/.]*', rooms)
            item['Rooms'] = room.group(0)
        
        studio = ' '.join(info_url.xpath('div[@class="details"]/div[@class="details_info"]/span[contains(@class, "detail_cell") and contains(text(), "studio")]/text()').extract()).strip()

        if (len(studio)>0 ):
            item['Beds'] = "0"

        beds = ' '.join(info_url.xpath('div[@class="details"]/div[@class="details_info"]/span[contains(@class, "detail_cell") and contains(text(), "bed")]/text()').extract()).strip()

        if( len(beds)>0 ):
            bed = re.search(r'[0-9/.]*', beds)
            item['Beds'] = bed.group(0)

        baths = ' '.join(info_url.xpath('div[@class="details"]/div[@class="details_info"]/span[contains(@class, "detail_cell") and contains(text(), "bath")]/text()').extract()).strip()
        if( len(baths)>0 ):
            bath = re.search(r'[0-9/.]*', baths)
            item['Baths'] = bath.group(0)
        
        pictures = response.xpath('//div[@class="no_select"]/ul[@class="image-gallery"]/li/img')
        picture_url = []
        for picture in pictures:
            picture_url.append(' '.join(picture.xpath('@data-original').extract()).strip())
            
        item['Picture'] = picture_url

        item['Abailibity'] = "Available now"

        div = response.xpath('//div[@class="left-three-fifths"]')
        for row in div:

            sections = row.xpath('section[@class="listings_sections"]')
            if len(sections) > 0:
                
                for section in sections:

                    description_detail = ' '.join(section.xpath('blockquote[@class="description_togglable hidden"]/text()').extract()).strip()
                    description = ' '.join(section.xpath('blockquote[@class="false"]/text()').extract()).strip()

                    if ( len(description_detail) > 0):
                        item['Description'] = description_detail
                    if ( len(description)> 0):
                        item['Description'] = description

                    
                    sub_sections = section.xpath('div[@class="amenities big_separator"]')
                    highlight_buff = []
                    amenitie_buff = []
                    for sub_section in sub_sections:
                        highlights = sub_section.xpath('ul/li/text()').extract()
                        if ( len(highlights) > 0 ):
                            
                            for highlight in highlights:
                                highlight_text = highlight.replace("\n","")

                                highlight_text = highlight_text.strip()
                                if highlight_text != "":
                                    highlight_buff.append(highlight_text)
                            
                        amenities = sub_section.xpath('div[@class="amenity-group"]/div[@class="third"]/ul/li/text()').extract()
                        if ( len(amenities) > 0 ):
                            
                            for amenitie in amenities:
                                amenitie_text = amenitie.replace("\n","")

                                amenitie_text = amenitie_text.strip()
                                if amenitie_text != "":
                                    amenitie_buff.append(amenitie_text)

                        if( (len(highlight_buff)>0) and (len(amenitie_buff)>0) ):
                            item['Amenities'] = highlight_buff + amenitie_buff
                        if( (len(highlight_buff)>0) and (len(amenitie_buff)==0) ):
                            item['Amenities'] = highlight_buff
                        if( (len(highlight_buff)==0) and (len(amenitie_buff)>0) ):
                            item['Amenities'] = amenitie_buff
        yield item
