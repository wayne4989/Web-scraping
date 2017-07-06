# -*- coding: utf-8 -*-
import scrapy
import useragent
from Datagrapplescraper.items import DatagrapplescraperItem
from scrapy.http import Request, FormRequest
from copy import deepcopy
from time import sleep
import time, re, random, base64, datetime
import csv, json


class DatagrapplespiderSpider(scrapy.Spider):
    name = "datagrapplespider"
    allowed_domains = ["datagrapple.com"]
    login_page = 'https://www.datagrapple.com/Account/Login'
    start_urls = (
        'https://www.datagrapple.com/Account/Login',
    )

    select_year = ""
    select_param = ""
    count = 0
    useragent_lists = useragent.user_agent_list

    def __init__(self,  year ='None', param='None', *args, **kwargs):

        super(DatagrapplespiderSpider, self).__init__(*args, **kwargs)
        
        self.select_param = param
        self.select_year = year

    def set_proxies(self, url, callback, headers=None, body=None):

        req = Request(url=url, method="POST", callback=callback, dont_filter=True, headers= headers, body=body)

        user_pass=base64.encodestring(b'username:password').strip().decode('utf-8')

        # http://your-proxy-server-address:proxy-port

        req.meta['proxy'] = "http://ofurgody.proxysolutions.net:11355"
        req.headers['Proxy-Authorization'] = 'Basic ' + user_pass
        user_agent = self.useragent_lists[random.randrange(0, len(self.useragent_lists))]
        req.headers['User-Agent'] = user_agent

        return req

    def parse(self, response):

        value = ''.join(response.xpath('//form/input[@name="__RequestVerificationToken"]/@value').extract()[0]).strip()

        # self.logger.info(value)

        yield scrapy.FormRequest(
        
            url="https://www.datagrapple.com/Account/Login",
            formdata={
                '__RequestVerificationToken': value,
                'UserName':'thomas1068',
                'Password':'dnflgmlakd888'
            },
            callback=self.after_login
        )

    def after_login(self, response):

        # check login succeed before going on
        if "The user name or password provided is incorrect." in response.body:
            self.logger.info("Login failed!!!")
            return
        else:
            self.logger.info("===================== Login Okay!!! ======================")
            self.clearLog()            
            years = [
                "1",
                "3",
                "5",
                "7",
                "10"
            ]

            headers = {
                'Accept':'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding':'gzip, deflate, br',
                'Accept-Language':'en-US,en;q=0.8',
                'Content-Type':'application/json; charset=UTF-8',
                'Host':'www.datagrapple.com',
                'Referer':'https://www.datagrapple.com/Home/Grapple',
                'X-Requested-With':'XMLHttpRequest',
            }

            # ipUrl = 'http://lumtest.com/myip.json'
            # proxy_ip_req = self.set_proxies(ipUrl, self.get_proxy_ip)
            # yield proxy_ip_req
            # return

            payload_list = []
            payload_list_all = []

            # read varid from csv file
            myfile = open("varidlist.csv", "rb")
            varidlist = csv.reader(myfile)


            if (self.select_year == "1" and self.select_param == "day"):

                self.logger.info("------------- 1Y Day payload ----------------")

                base_payload = {"IdTree":10030,"IdNode":"1544","Maturity":"1","RequestSpan":{"Span":1,"GrappleSpanType":"Day"},"GraphType":"HistoGraph"}

                for i, varid in enumerate(varidlist):

                    base_payload['IdNode'] = ''.join(varid).strip()

                    payload_list.append(deepcopy(base_payload))

                for onepay in payload_list:
                    # self.logger.info(onepay)               

                    url = 'https://www.datagrapple.com/api/GraphGrappleRequest/'

                    req = self.set_proxies(url, self.getJson, headers, json.dumps(onepay))
                    req.meta['years'] = onepay['Maturity']

                    yield req  

                    # return

            elif (self.select_year == "3" and self.select_param == "day"):

                self.logger.info("------------- 3Y Day payload ----------------")

                base_payload = {"IdTree":10030,"IdNode":"1544","Maturity":"3","RequestSpan":{"Span":1,"GrappleSpanType":"Day"},"GraphType":"HistoGraph"}

                for i, varid in enumerate(varidlist):

                    base_payload['IdNode'] = ''.join(varid).strip()

                    payload_list.append(deepcopy(base_payload))

                for onepay in payload_list:
                    # self.logger.info(onepay)               

                    url = 'https://www.datagrapple.com/api/GraphGrappleRequest/'

                    req = self.set_proxies(url, self.getJson, headers, json.dumps(onepay))
                    req.meta['years'] = onepay['Maturity']

                    yield req  

                    # return

            elif (self.select_year == "5" and self.select_param == "day"):

                self.logger.info("------------- 5Y Day payload ----------------")

                base_payload = {"IdTree":10030,"IdNode":"1544","Maturity":"5","RequestSpan":{"Span":1,"GrappleSpanType":"Day"},"GraphType":"HistoGraph"}

                for i, varid in enumerate(varidlist):

                    base_payload['IdNode'] = ''.join(varid).strip()

                    payload_list.append(deepcopy(base_payload))

                for onepay in payload_list:
                    # self.logger.info(onepay)               

                    url = 'https://www.datagrapple.com/api/GraphGrappleRequest/'

                    req = self.set_proxies(url, self.getJson, headers, json.dumps(onepay))
                    req.meta['years'] = onepay['Maturity']

                    yield req 

                    # return

            elif (self.select_year == "7" and self.select_param == "day"):

                self.logger.info("------------- 7Y Day payload ----------------")

                base_payload = {"IdTree":10030,"IdNode":"1544","Maturity":"7","RequestSpan":{"Span":1,"GrappleSpanType":"Day"},"GraphType":"HistoGraph"}

                for i, varid in enumerate(varidlist):

                    base_payload['IdNode'] = ''.join(varid).strip()

                    payload_list.append(deepcopy(base_payload))

                for onepay in payload_list:
                    # self.logger.info(onepay)               

                    url = 'https://www.datagrapple.com/api/GraphGrappleRequest/'

                    req = self.set_proxies(url, self.getJson, headers, json.dumps(onepay))
                    req.meta['years'] = onepay['Maturity']

                    yield req 

                    # return

            elif (self.select_year == "10" and self.select_param == "day"):

                self.logger.info("------------- 10Y Day payload ----------------")

                base_payload = {"IdTree":10030,"IdNode":"1544","Maturity":"10","RequestSpan":{"Span":1,"GrappleSpanType":"Day"},"GraphType":"HistoGraph"}

                for i, varid in enumerate(varidlist):

                    base_payload['IdNode'] = ''.join(varid).strip()

                    payload_list.append(deepcopy(base_payload))

                for onepay in payload_list:
                    # self.logger.info(onepay)               

                    url = 'https://www.datagrapple.com/api/GraphGrappleRequest/'

                    req = self.set_proxies(url, self.getJson, headers, json.dumps(onepay))
                    req.meta['years'] = onepay['Maturity']

                    yield req

            elif (self.select_year == "all" and self.select_param == "day"):

                self.logger.info("================  Get day data for all durations =================")

                base_payload = {"IdTree":10030,"IdNode":"1544","Maturity":"10","RequestSpan":{"Span":1,"GrappleSpanType":"Day"},"GraphType":"HistoGraph"}

                for i, varid in enumerate(varidlist):

                    base_payload['IdNode'] = ''.join(varid).strip()

                    payload_list.append(deepcopy(base_payload))

                for payload in payload_list:

                    for year_count in xrange(0,5):

                        payload['Maturity'] = int(years[year_count])
                        # self.logger.info(payload)  

                        payload_list_all.append(deepcopy(payload))

                for onepay in payload_list_all:

                    url = 'https://www.datagrapple.com/api/GraphGrappleRequest/'

                    req = self.set_proxies(url, self.getJson, headers, json.dumps(onepay))
                    req.meta['years'] = onepay['Maturity']

                    yield req  

                    # return

            elif (self.select_year == "1" and self.select_param == "week"):

                self.logger.info("------------- 1Y Week payload ----------------")

                base_payload = {"IdTree":10030,"IdNode":"1544","Maturity":"1","RequestSpan":{"Span":1,"GrappleSpanType":"Week"},"GraphType":"HistoGraph"}

                for i, varid in enumerate(varidlist):

                    base_payload['IdNode'] = ''.join(varid).strip()

                    payload_list.append(deepcopy(base_payload))

                for onepay in payload_list:
                    # self.logger.info(onepay)               

                    url = 'https://www.datagrapple.com/api/GraphGrappleRequest/'

                    req = self.set_proxies(url, self.getJson, headers, json.dumps(onepay))
                    req.meta['years'] = onepay['Maturity']

                    yield req  

                    # return

            elif (self.select_year == "3" and self.select_param == "week"):

                self.logger.info("------------- 3Y Week payload ----------------")

                base_payload = {"IdTree":10030,"IdNode":"1544","Maturity":"3","RequestSpan":{"Span":1,"GrappleSpanType":"Week"},"GraphType":"HistoGraph"}

                for i, varid in enumerate(varidlist):

                    base_payload['IdNode'] = ''.join(varid).strip()

                    payload_list.append(deepcopy(base_payload))

                for onepay in payload_list:
                    # self.logger.info(onepay)               

                    url = 'https://www.datagrapple.com/api/GraphGrappleRequest/'

                    req = self.set_proxies(url, self.getJson, headers, json.dumps(onepay))
                    req.meta['years'] = onepay['Maturity']

                    yield req 

                    # return

            elif (self.select_year == "5" and self.select_param == "week"):

                self.logger.info("------------- 5Y Week payload ----------------")

                base_payload = {"IdTree":10030,"IdNode":"1544","Maturity":"5","RequestSpan":{"Span":1,"GrappleSpanType":"Week"},"GraphType":"HistoGraph"}

                for i, varid in enumerate(varidlist):

                    base_payload['IdNode'] = ''.join(varid).strip()

                    payload_list.append(deepcopy(base_payload))

                for onepay in payload_list:
                    # self.logger.info(onepay)               

                    url = 'https://www.datagrapple.com/api/GraphGrappleRequest/'

                    req = self.set_proxies(url, self.getJson, headers, json.dumps(onepay))
                    req.meta['years'] = onepay['Maturity']

                    yield req 

                    # return

            elif (self.select_year == "7" and self.select_param == "week"):

                self.logger.info("------------- 7Y Week payload ----------------")

                base_payload = {"IdTree":10030,"IdNode":"1544","Maturity":"7","RequestSpan":{"Span":1,"GrappleSpanType":"Week"},"GraphType":"HistoGraph"}

                for i, varid in enumerate(varidlist):

                    base_payload['IdNode'] = ''.join(varid).strip()

                    payload_list.append(deepcopy(base_payload))

                for onepay in payload_list:
                    # self.logger.info(onepay)               

                    url = 'https://www.datagrapple.com/api/GraphGrappleRequest/'

                    req = self.set_proxies(url, self.getJson, headers, json.dumps(onepay))
                    req.meta['years'] = onepay['Maturity']

                    yield req 

                    # return

            elif (self.select_year == "10" and self.select_param == "week"):

                self.logger.info("------------- 10Y Week payload ----------------")

                base_payload = {"IdTree":10030,"IdNode":"1544","Maturity":"10","RequestSpan":{"Span":1,"GrappleSpanType":"Week"},"GraphType":"HistoGraph"}

                for i, varid in enumerate(varidlist):

                    base_payload['IdNode'] = ''.join(varid).strip()

                    payload_list.append(deepcopy(base_payload))

                for onepay in payload_list:
                    # self.logger.info(onepay)               

                    url = 'https://www.datagrapple.com/api/GraphGrappleRequest/'

                    req = self.set_proxies(url, self.getJson, headers, json.dumps(onepay))
                    req.meta['years'] = onepay['Maturity']

                    yield req 

                    # return
            elif (self.select_year == "all" and self.select_param == "week"):

                self.logger.info("================ Get week data for all durations =================")

                base_payload = {"IdTree":10030,"IdNode":"1544","Maturity":"10","RequestSpan":{"Span":1,"GrappleSpanType":"Week"},"GraphType":"HistoGraph"}

                for i, varid in enumerate(varidlist):

                    base_payload['IdNode'] = ''.join(varid).strip()

                    payload_list.append(deepcopy(base_payload))

                for payload in payload_list:

                    for year_count in xrange(0,5):

                        payload['Maturity'] = int(years[year_count])
                        # self.logger.info(payload)  

                        payload_list_all.append(deepcopy(payload))

                for onepay in payload_list_all:

                    url = 'https://www.datagrapple.com/api/GraphGrappleRequest/'

                    req = self.set_proxies(url, self.getJson, headers, json.dumps(onepay))
                    req.meta['years'] = onepay['Maturity']

                    yield req  

                    # return

            # Get all data
            elif (self.select_year == "all" and self.select_param == "max"):

                self.logger.info("================ All get data =================")

                base_payload = {"IdTree":10030,"IdNode":"114","Maturity":5,"RequestSpan":{"GrappleSpanType":"Max"},"GraphType":"HistoGraph"}

                for i, varid in enumerate(varidlist):

                    base_payload['IdNode'] = ''.join(varid).strip()

                    payload_list.append(deepcopy(base_payload))

                for payload in payload_list:

                    for year_count in xrange(0,5):

                        payload['Maturity'] = int(years[year_count])
                        # self.logger.info(payload)  

                        payload_list_all.append(deepcopy(payload))

                for onepay in payload_list_all:

                    url = 'https://www.datagrapple.com/api/GraphGrappleRequest/'

                    req = self.set_proxies(url, self.getJson, headers, json.dumps(onepay))
                    req.meta['years'] = onepay['Maturity']

                    yield req  

                    # return

            # Get data for selected year
            elif (self.select_year == "1" or self.select_year == "3" or self.select_year == "5" or self.select_year == "7" or self.select_year == "10" and self.select_param == "max"):

                self.logger.info("================ " + "Get data of " + self.select_year + "Y =================")

                base_payload = {"IdTree":10030,"IdNode":"114","Maturity":5,"RequestSpan":{"GrappleSpanType":"Max"},"GraphType":"HistoGraph"}
                   
                for i, varid in enumerate(varidlist):

                    base_payload['IdNode'] = ''.join(varid).strip()

                    payload_list.append(deepcopy(base_payload))

                result_year = int(self.select_year)
                # self.logger.info(result_year)

                for payload in payload_list:

                    payload['Maturity'] = result_year
                    # self.logger.info(payload)  

                    url = 'https://www.datagrapple.com/api/GraphGrappleRequest/'

                    req = self.set_proxies(url, self.getJson, headers, json.dumps(payload))
                    req.meta['years'] = result_year

                    yield req

                    # return
            else:
                print("===== Please Insert Correct Command!!! =====")
                print(" - Case in 1day for 1y : scrapy crawl datagrapplespider -a year=1 -a param=day")
                print(" - Case in 1day for 3y : scrapy crawl datagrapplespider -a year=3 -a param=day")
                print(" - Case in 1day for 5y : scrapy crawl datagrapplespider -a year=5 -a param=day")
                print(" - Case in 1day for 7y : scrapy crawl datagrapplespider -a year=7 -a param=day")
                print(" - Case in 1day for 7y : scrapy crawl datagrapplespider -a year=7 -a param=day")
                print(" - Case in 1day for all : scrapy crawl datagrapplespider -a year=all -a param=day")
                print(" - Case in 1week for 1y : scrapy crawl datagrapplespider -a year=1 -a param=week")
                print(" - Case in 1week for 3y : scrapy crawl datagrapplespider -a year=3 -a param=week")
                print(" - Case in 1week for 5y : scrapy crawl datagrapplespider -a year=5 -a param=week")
                print(" - Case in 1week for 7y : scrapy crawl datagrapplespider -a year=7 -a param=week")
                print(" - Case in 1week for 10y : scrapy crawl datagrapplespider -a year=10 -a param=week")
                print(" - Case in 1week for all : scrapy crawl datagrapplespider -a year=all -a param=week")
                print(" - Case in get all data : scrapy crawl datagrapplespider -a year=all -a param=max")
                print(" - Case in get data for selected year : scrapy crawl datagrapplespider -a year=selected year(ex: if 1y, year=1) -a param=all")
                return

    def getJson(self, response):

        self.logger.info("-------------- getJson -------------")
        self.logger.info(self.count)
        self.count = self.count + 1

        years = response.meta['years']

        item = DatagrapplescraperItem()
        json_data = json.loads(response.body)
        log_varid = ""
        if "HistoLines" in json_data:

            # test
            # count = 0

            for every in json_data["HistoLines"][0]:

                a = every["ValueDate"]
                b=re.search(r'/Date\((.*?)\)/',a)
                c=b.group(1).replace("000-0000","")
                dt = datetime.datetime.fromtimestamp(float(c))
                vardate = dt.strftime('%Y-%m-%d %H:%M:%S')                
                item['vardate'] = vardate

                item['deltaspread'] = every["DeltaSpread"]
                item['spread'] = every["Spread"]
                item['varid'] = every["IdParent"]
                item['dailyvol'] = every["DailyVol"]
                item['vardur'] = years
                log_varid = every["IdParent"]
                yield item

                # test
                # count = count + 1
                # if count > 4:
                #     return
        log_txt = "varid=" + str(log_varid) + ", year=" + str(years) + ", param=" + self.select_param
        self.makeLog(log_txt)

    def makeLog(self, txt):

        standartdate = datetime.datetime.now()
        date = standartdate.strftime('%Y-%m-%d %H:%M:%S')
        fout = open("log.txt", "a")
        fout.write(str(date) + " -> " + txt + "\n")
        fout.close()

    def clearLog(self):
        fout = open("log.txt", "w")
        fout.close()

    def get_proxy_ip(self, response):
        print response.body