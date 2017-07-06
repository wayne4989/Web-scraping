# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
from Dukascopyscraper.items import DukascopyscraperItem
import time, re, json, base64, os

class DukascopyspiderSpider(scrapy.Spider):
    name = "dukascopyspider"

    start_date = ""
    last_date = ""

    def __init__(self,  start_date='', last_date='', *args, **kwargs):

        super(DukascopyspiderSpider, self).__init__(*args, **kwargs)
        
        self.start_date = start_date
        self.last_date = last_date

    def start_requests(self):
        self.logger.info("============= Start ============")

        headers = {
            'referer':'https://freeserv.dukascopy.com/2.0/?path=economic_calendar_new/index&showHeader=false&tableBorderColor=%23D92626&defaultTimezone=0&defaultCountries=c%3AAU%2CCA%2CCH%2CCN%2CEU%2CGB%2CJP%2CNZ%2CUS%2CDE%2CFR%2CIT%2CES&impacts=0%2C1%2C2&dateTab=2&dateFrom=1464480000000&dateTo=1464998400000&showColCountry=true&showColCurrency=true&showColImpact=true&showColPrevious=true&showColForecast=true&width=100%25&height=500&adv=popup',
        }

        pattern = '%Y.%m.%d'
        os.environ['TZ']='UTC'

        startDate = int(time.mktime(time.strptime(self.start_date,pattern)))
        lastDate = int(time.mktime(time.strptime(self.last_date,pattern)))
  
        url = "https://freeserv.dukascopy.com/2.0/index.php?path=economic_calendar_new%2FgetNews&since=" + str(startDate) + "000" + "&until=" + str(lastDate) + "000" + "&jsonp=_callbacks____4j48ucily"

        req = Request(url=url, callback=self.getData,dont_filter=True, headers=headers)

        yield req

    def getData(self, response):
        self.logger.info("============ Get Data ============")

        item = DukascopyscraperItem()

        sub_data = re.search("_callbacks____4j48ucily\((.*\])\)", response.body, re.M|re.S).group(1)
        jsonData = json.loads(sub_data)

        for element in jsonData:

            item['Date'] =  element['date']
            item['Actual'] =  element['actual']
            item['Country'] =  element['country']
            item['Currency'] =  element['currency']
            item['Periodicity'] =  element['periodicity']
            item['Previous'] =  element['previous']
            item['Title'] =  element['title']
            item['Forecast'] =  element['forecast']

            yield item
