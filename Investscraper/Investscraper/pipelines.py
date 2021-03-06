# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.utils.project import get_project_settings
from twisted.enterprise import adbapi 

settings = get_project_settings()

class InvestscraperPipeline(object):

    insert_sql = """insert into 3M_data (%s) values ( %s )"""
    
    def __init__(self):    
        dbargs = settings.get('DB_CONNECT')    
        db_server = settings.get('DB_SERVER')    
        dbpool = adbapi.ConnectionPool(db_server, **dbargs)    
        self.dbpool = dbpool    
 
    def __del__(self):    
        self.dbpool.close()    
 
    def process_item(self, item, spider):
        self.insert_data(item,self.insert_sql)
        return item    
 
    def insert_data(self, item, insert):    
        keys = item.fields.keys()    
        fields = u','.join(keys)    
        qm = u','.join([u'%s'] * len(keys))    
        print qm
        sql = insert % (fields, qm)
        data = [item[k] for k in keys]
        return self.dbpool.runOperation(sql, data)