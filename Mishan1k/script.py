#!/usr/local/bin/python3.7
from sqlalchemy.orm import sessionmaker
from scrapy_spider.models import QuoteDB, db_connect, create_table

def find_quotes(author_name):

    list_of_quotes = []

    for quote in session.query(QuoteDB.quote).filter(QuoteDB.author == author_name):
        list_of_quotes.append(quote)
    if ( len(list_of_quotes) == 0):
        print ("Not found")
    print(list_of_quotes)

author_name = input("Enter author full name, whose quotes you want to recieve : ").strip()
engine = db_connect()
create_table(engine)
Session = sessionmaker(bind=engine)
session = Session()
find_quotes(author_name)
session.close()
