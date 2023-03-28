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
    for order in orders:
        if order not in db_orders:
            database.add(order)
        if order.state == OrderState.OPEN:
            parse_order(order)


def parse_order(order):
    account_dict = {}
    for item in order.items:
        if item.account_id not in account_dict:
            account_dict.setdefault(item.account_id, []).append(item)     
        else:
            account_dict.setdefault(item.account_id, []).extend([item])
    counter = 0
    for key in account_dict:
        counter += 1
        parent_id = order.id
        order_id = parent_id + "-" + str(counter)
        subtotal = 0
        for value in account_dict[key]:
            subtotal += value.price
        taxes = subtotal * .0825        # calculate this later using tax rate
        service_fee = 0                 # calculate this later using service fee %
        credit_fee = 0                  # caluclate this later using credit fee %

        '''
        new time stamp for when this sub order process is done.
        if we want to keep Square API time stamp we can remove
        '''
        tz_utc = pytz.utc
        created_at = datetime.now(tz_utc)
        # create new object for email use
        order_object_to_email = Order(order_id, key, OrderState.OPEN,
                                        subtotal, taxes,
                                        service_fee, credit_fee,
                                        created_at, account_dict[key],
                                        parent_id)
        # test print
        print('\n')
        print(order_object_to_email)
        print(order_object_to_email.id)
        print(order_object_to_email.parent_id)
        print(order_object_to_email.state)
        print(order_object_to_email.subtotal)
        print(order_object_to_email.taxes)
        print(order_object_to_email.service_fee)
        print(order_object_to_email.credit_fee)
        print(order_object_to_email.created_at)
        print(order_object_to_email.items)
        for item in order_object_to_email.items:
            print(item.name)
    return order_object_to_email


if __name__ == "__main__": 
    with app.app_context():
        main()