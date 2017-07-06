# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request

class CarimagescraperPipeline(object):
    def process_item(self, item, spider):
        return item

class MyImagesPipeline(ImagesPipeline):
    
    def file_path(self, request, response=None, info=None):
        filename = request.url.split('/')[-1]
        return "%s/%s" % (request.meta['dir_name'], filename)

    def get_media_requests(self, item, info):
        for ind, image in enumerate(item['image_urls']):
            if (ind==0): continue
            req = Request(image)
            req.meta['dir_name'] = str(int(ind / 2000))
            yield req