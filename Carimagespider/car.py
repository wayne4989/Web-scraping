import csv
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common import exceptions as EX
from time import sleep
from bs4 import BeautifulSoup
from re import compile, findall
from scrapex import *

sc = Scraper(
    use_cache=False,
    timeout=300,
    retries = 3
    )

def main():

    global driver

    driver = webdriver.Chrome()
    page = 1
    while True:
        print ("http://www.factorypreownedcollection.com/VehicleSearchResults?pageNo=%d" % (page))
        driver.get("http://www.factorypreownedcollection.com/VehicleSearchResults?pageNo=%d" % (page))
        if page ==1:
            inputElement = driver.find_element_by_id("cs:zip")
            inputElement.send_keys('18002')
            inputElement.send_keys(Keys.ENTER)
            
        try:
            WebDriverWait(driver, 100).until(EC.text_to_be_present_in_element((By.XPATH, '//a[@class="pagination-button  selected"]'), str(page)))
        except:
            break

        html_doc = Doc(html=driver.page_source)
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '//section[@id="vehicleSearchResult"]')))
        get_depart_of_items(html_doc)

        page = page + 1
        print page
        sleep(1)

    driver.quit()

def get_depart_of_items(html_doc):
    print "Get Depart of Items:     =============> Processing"

    li_items = html_doc.q('//section[@id="vehicleSearchResult"]//section[contains(@class,"card insight vehicle-card")]')
    print "*********************"

    for idx, row in enumerate(li_items):
        parent_url = row.x('div[@class="content"]/div[@class="link"]/a/@href').trim()
        print "=====> progress %s : %s " % (str(idx), parent_url)
        driver.get(parent_url)
        sleep(2)
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '//section[@id="photoCarousel"]')))
        item_doc = Doc(html=driver.page_source)
        get_img_url(item_doc, parent_url)       

    print "==> Row End"

def get_img_url(item_doc, CheckURL):

    li_items = item_doc.q('//img[@not="href"]')
    print len(li_items)

    for itemurl in li_items:
        imgUrl = itemurl.x('@data-src').trim()
        if imgUrl=="":
            imgUrl = itemurl.x('@src').trim()
        print("-------------------------")
        print imgUrl

        if imgUrl:

            sc.save(["ImageURL",imgUrl, "CheckURL", CheckURL],'imgUrl1.csv')  

if __name__ == '__main__':

    main()