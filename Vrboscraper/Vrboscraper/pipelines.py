# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

class VrboscraperPipeline(object):

    def __init__(self):
        self.church_seen = set()
        
    def process_item(self, item, spider):
        churchid = (item['ID'] if item['ID'] else '') + (item['Description'] if item['Description'] else '') + (item['Location'] if item['Location'] else '')
        if churchid in self.church_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.church_seen.add(churchid)
            return item