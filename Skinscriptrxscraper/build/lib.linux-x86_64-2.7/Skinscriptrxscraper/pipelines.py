# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

class SkinscriptrxscraperPipeline(object):

    def __init__(self):
        self.skinrx_seen = set()

    def process_item(self, item, spider):
        skinrxid = (item['Name'] if item['Name'] else '') + (item['Phone'] if item['Phone'] else '') + (item['Address1'] if item['Address1'] else '')
        if skinrxid in self.skinrx_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.skinrx_seen.add(skinrxid)
            return item