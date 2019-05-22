# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from scrapy_spider.models import QuoteDB, db_connect, create_table
from script import find_quotes
list_of_quotes = []

class ScrapySpiderPipeline(object):
    def __init__(self):
        """
            Initializes database connection and sessionmaker.
            Creates deals table.
            """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
    
    def process_item(self, item, spider):
        """Save deals in the database.
            This method is called for every item pipeline component.
            """
        session = self.Session()
        quotedb = QuoteDB()
        quotedb.quote = item["quote"]
        quotedb.author = item["author"]
        
        try:
            session.add(quotedb)
            session.commit()
                
                # find_quotes()
                #for quote in session.query(QuoteDB.quote).filter(QuoteDB.author=='Albert Einstein'):
                # print (quote)

        except:
            session.rollback()
            raise
        finally:
            
            print(list_of_quotes)
            session.close()
        
        
        return item

    def close_spider(self, spider):
        session = self.Session()
        while True:
            name = input("Enter author full name, whose quotes you want to recieve : ").strip()
            if name == 'stop':
                break
            find_quotes(name)
        session.close()


