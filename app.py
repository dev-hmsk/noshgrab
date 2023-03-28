from api.web import Square
from database.model import db, Order, Item, OrderState
from flask import Flask
from database.managers import NoshGrab
from api.web import Square
from config.config import CONFIG
from datetime import datetime
import pytz
import os

app = Flask(__name__)

db_config = CONFIG.info['database']
app.config['SQLALCHEMY_DATABASE_URI'] = f'{db_config["dialect"]}://{db_config["user"]}:{os.environ["DB_PASS"]}@{db_config["ip"]}:{db_config["port"]}/{db_config["name"]}'

db.init_app(app)

def main():
    web_s = Square()
    database = NoshGrab(db)
    web_s.connect(os.environ['TOKEN'], environment=CONFIG.info['square']['environment'])
    orders = web_s.get_orders()
    db_orders = database.get.orders()

    # Check for every order from Square. Check if order is in the database list of orders from database.get.orders()
    order_list = []
    for order in orders:
        if order not in db_orders:
            database.add(order)
            if order.state == OrderState.OPEN:
                print('parsing orders', order.id)
                order_list.append(parse_order(order))
    # write function to add sub orders to database.
    for order in order_list:
        for sub_order in order:
            print(f'adding {sub_order.id}')
            database.add(sub_order)

def parse_order(order):
    account_dict = {}
    for item in order.items:
        if item.account_id not in account_dict:
            account_dict[item.account_id] = [item]
        else:
            account_dict[item.account_id].append(item)
    order_list = []
    counter = 0
    for account_id, items in account_dict.items():
        counter += 1
        parent_id = order.id
        order_id = parent_id + "-" + str(counter)
        subtotal = 0
        for item in items:
            subtotal += item.price
        taxes = subtotal * .0825        # calculate this later using tax rate
        service_fee = 0                 # calculate this later using service fee %
        credit_fee = 0                  # caluclate this later using credit fee %
        created_at = order.created_at
        # create new object for email use
        order_object_to_email = Order(order_id, account_id, OrderState.OPEN,
                                    subtotal, taxes,
                                    service_fee, credit_fee,
                                    created_at, items,
                                    parent_id)
        order_list.append(order_object_to_email)

    return order_list


if __name__ == "__main__": 
    with app.app_context():
        main()