# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.utils.project import get_project_settings
from twisted.enterprise import adbapi 
from items import DataItem,  ChartItem

settings = get_project_settings()

class IeconomicsPipeline(object):

    insert_first_table_sql = """insert into first_table (%s) values ( %s )"""
    insert_iconomics_data_sql = """insert into iconomics_data (%s) values ( %s )"""
    
    def __init__(self):    
        dbargs = settings.get('DB_CONNECT')    
        db_server = settings.get('DB_SERVER')    
        dbpool = adbapi.ConnectionPool(db_server, **dbargs)    
        self.dbpool = dbpool    
 
    def __del__(self):    
        self.dbpool.close()    
 
    def process_item(self, item, spider):
    	
        if isinstance(item, DataItem):
            self.insert_data(item,self.insert_iconomics_data_sql)

        elif isinstance(item, ChartItem):
            self.insert_data(item, self.insert_first_table_sql)

        return item    
 
    def insert_data(self, item, insert):    
        keys = item.fields.keys()    
        fields = u','.join(keys)    
        qm = u','.join([u'%s'] * len(keys))    
        sql = insert % (fields, qm)
        data = [item[k] for k in keys]
        return self.dbpool.runOperation(sql, data)