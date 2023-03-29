from api.web import Square
from database.model import db, Order, OrderState
from flask import Flask
from database.managers import NoshGrab
from api.web import Square
from config.config import CONFIG
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
    account_list = web_s.get_accounts()

    order_list = []
    json_list = []
    for order in orders:
        if order not in db_orders:
            database.add(order)
        if order.state == OrderState.OPEN:
            # print('parsing orders', order.id)
            order_list.append(parse_order(order))

    for order in order_list:
        for sub_order in order:
            if sub_order not in db_orders:
                print(f'adding {sub_order.id}')
                database.add(sub_order)
    
    # do not indent. this recreates above for loop within the function. We can change this later if need be.
    # i am currently working to nest this within above for loop in future commit.
    json_list.append(create_json_email(account_list, order_list))

    print(order_list)
    print(json_list)


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


def create_json_email(account_list, order_list):
    json_email_list = []
    account_dict = {}
    for account in account_list:
        account_dict[account.id] = [account.id, account.name,
                                    account.email, account.address,
                                    account.locality, account.state,
                                    account.postal, account.country]
    for order in order_list:
        for sub_order in order:
            item_dict = {}
            for item in sub_order.items:
                if item.id not in item_dict:
                    item_dict[item.id] = [item.id, item.version, item.account_id, item.name, item.price]
                else:
                    item_dict[item.id].append(item.id, item.version, item.account_id, item.name, item.price)
            
            if sub_order.account_id in account_dict:
                json_email_dict = {sub_order.id:{'Order_ID': sub_order.id,
                                                 'Account_ID': sub_order.account_id,
                                                 'Account_Name': account_dict[sub_order.account_id][1],
                                                 'Account_Email': account_dict[sub_order.account_id][2],
                                                 'Account_Address': account_dict[sub_order.account_id][3],
                                                 'Items': item_dict,
                                                 'Quantity of each Item': None, # <--- This is not currently ITEM() attr. But is given by get_orders API call
                                                 'Taxes': sub_order.taxes,
                                                 'Sub_Total': sub_order.subtotal,
                                                 'Service Charge': sub_order.subtotal * .20,
                                                 'Credit Card Fee': (sub_order.subtotal + sub_order.taxes) *.029}}
                
                json_email_list.append(json_email_dict)

    return json_email_list


if __name__ == "__main__": 
    with app.app_context():
        main()