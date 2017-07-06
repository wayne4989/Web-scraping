# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.utils.project import get_project_settings
from twisted.enterprise import adbapi 
from items import EquitiesItem, DirectorsItem, SymbolsItem, DealingsItem, IncomesItem, CashFlowsItem, BalancesItem, ForecastsItem, HistoricalItem

settings = get_project_settings()

class FtscraperPipeline(object):

    insert_equities_data_sql = """insert into equities_data (%s) values ( %s )"""
    insert_symbols_data_sql = """insert into symbols_data (%s) values ( %s )"""
    insert_directors_data_sql = """insert into directors_data (%s) values ( %s )"""
    insert_dealings_data_sql = """insert into dealings_data (%s) values ( %s )"""
    insert_incomes_data_sql = """insert into incomes_data (%s) values ( %s )"""
    insert_cashflows_data_sql = """insert into cashflows_data (%s) values ( %s )"""
    insert_balances_data_sql = """insert into balances_data (%s) values ( %s )"""
    insert_forecast_data_sql = """insert into forecast_data (%s) values ( %s )"""
    insert_historical_data_sql = """insert into historical_data (%s) values ( %s )"""
    
    def __init__(self):    
        dbargs = settings.get('DB_CONNECT')    
        db_server = settings.get('DB_SERVER')    
        dbpool = adbapi.ConnectionPool(db_server, **dbargs)    
        self.dbpool = dbpool    
 
    def __del__(self):    
        self.dbpool.close()    
 
    def process_item(self, item, spider):
        
        if isinstance(item, EquitiesItem):
            self.insert_data(item,self.insert_equities_data_sql)

        elif isinstance(item, SymbolsItem):
            self.insert_data(item, self.insert_symbols_data_sql)

        elif isinstance(item, DirectorsItem):
            self.insert_data(item, self.insert_directors_data_sql)

        elif isinstance(item, DealingsItem):
            self.insert_data(item, self.insert_dealings_data_sql) 

        elif isinstance(item, IncomesItem):
            self.insert_data(item, self.insert_incomes_data_sql) 

        elif isinstance(item, CashFlowsItem):
            self.insert_data(item, self.insert_cashflows_data_sql) 

        elif isinstance(item, BalancesItem):
            self.insert_data(item, self.insert_balances_data_sql) 

        elif isinstance(item, ForecastsItem):
            self.insert_data(item, self.insert_forecast_data_sql) 

        elif isinstance(item, HistoricalItem):
            self.insert_data(item, self.insert_historical_data_sql)   
                      
        return item    
 
    def insert_data(self, item, insert):    
        keys = item.fields.keys()    
        fields = u','.join(keys)    
        qm = u','.join([u'%s'] * len(keys))    
        sql = insert % (fields, qm)
        data = [item[k] for k in keys]
        return self.dbpool.runOperation(sql, data)