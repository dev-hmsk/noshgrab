#!/bin/env

from config.config import CONFIG
from database.model import db
from flask import Flask
from database.model import Order, Item, Account, OrderedItem
from database.managers import NoshGrab
from api.web import Square
import argparse
import os

app = Flask(__name__)

db_config = CONFIG.info['database']
db_uri = f'{db_config["dialect"]}://{db_config["user"]}:{os.environ["DB_PASS"]}@{db_config["ip"]}:{db_config["port"]}/{db_config["name"]}'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

db.init_app(app)

def main():
    parser = argparse.ArgumentParser("Database Updating Script")
    parser.add_argument('-D', '--drop-all', action='store_true', dest='drop_all',
                        help='Drop All Tables')
    parser.add_argument('-C', '--create-all', action='store_true', dest='create_all',
                        help='Create All Tables')
    parser.add_argument('-i', '--initialize', action='store_true', dest='initialize',
                        help='Add data from Web API')

    args = parser.parse_args()

    if args.drop_all:
        print("Dropping all tables")
        Account.__table__.drop(db.engine)
        OrderedItem.__table__.drop(db.engine)
        Item.__table__.drop(db.engine)
        Order.__table__.drop(db.engine)
        
    elif args.create_all:
        print("Creating all tables")
        db.create_all()

    elif args.initialize:
        web_s = Square()
        database = NoshGrab(db)
        web_s.connect(os.environ['TOKEN'], environment=CONFIG.info['square']['environment'])

        print('Adding Accounts')
        
        for account in web_s.get_accounts():
            database.add(account)
        
        print('Adding Items')
        
        for item in web_s.get_items():
            database.add(item)
        
        print('Adding Orders')

        for order in web_s.get_orders():
            # Skip this one order to give more tests cases when adding orders
            if order.id == 'TABsvHlgeYGEVx1JKa0aVE4OBBGZY':
                continue
            
            database.add(order)

if __name__ == "__main__": 
    with app.app_context():
        main()