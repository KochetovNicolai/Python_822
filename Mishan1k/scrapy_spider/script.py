#!/usr/local/bin/python3.7
from sqlalchemy.orm import sessionmaker
from models import QuoteDB, db_connect, create_table

def find_quotes (list_of_quotes):
    for quote in session.query(QuoteDB.quote).filter(QuoteDB.author == author_name):
        list_of_quotes.append(quote)
    if ( len(list_of_quotes) == 0):
        print ("Not found")


author_name = input("Enter author full name, whose quotes you want to recieve : ")

engine = db_connect()
create_table(engine)
self.Session = sessionmaker(bind=engine)
list_of_quotes = []
find_quotes (list_of_quotes)
print(list_of_quotes)


session.close()
