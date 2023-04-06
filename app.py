import json
import os
from api.web import Square
from database.model import db, Order, OrderState
from flask import Flask
from database.managers import NoshGrab
from api.web import Square
from config.config import CONFIG

from api.email import ASes
from database.model import OrderState, Order

app = Flask(__name__)

db_config = CONFIG.info['database']
app.config['SQLALCHEMY_DATABASE_URI'] = f'{db_config["dialect"]}://{db_config["user"]}:{os.environ["DB_PASS"]}@{db_config["ip"]}:{db_config["port"]}/{db_config["name"]}'

db.init_app(app)

def main():
    web_s = Square()
    database = NoshGrab(db)
    web_s.connect(os.environ['TOKEN'], environment=CONFIG.info['square']['environment'])

    '''
    For testing purposes: Drop and then Create all database tables.

    The below logic assumes that as new orders come in we will check against the database,
    add the order if not present in database, then check OrderState.
    If OPEN we parse_order(order). This is then appended to an order_list[].
    Then for every order in the order_list, we loop for every sub_order,
    and add them as novel orders to the database.print(item.id, item.name, item.quantity)
    We then run create_json_email() and pass in the iterated sub_order
    with the account_list given to us by web_s.get_accounts().

    This will allow us to create a novel JSON for every sub_order 
    which will have the relevant info needed to send out 
    an automated email to the apprioriate account
    '''
    orders = web_s.get_orders()
    db_orders = database.get.orders()
    account_list = web_s.get_accounts()

    order_list = []
    json_list = []
    account_dict = {}

    for account in account_list:
        account_dict[account.id] = account

    for account in account_list:
        database.add(account)
        
    for order in orders:
        if order not in db_orders:
            database.add(order)
            if order.state == OrderState.OPEN:
                print('parsing orders', order.id)
                order_list.append(parse_order(order))

    for order in order_list:
        for sub_order in order:
            if sub_order not in db_orders:
                print(f'adding {sub_order.id}')
                database.add(sub_order)
                json_list.append(create_json_email(account_dict, sub_order))
    
    email = ASes(CONFIG.info['email'])
    email.load_template('order_invoice.html')

    for order in json_list:
        html = email.render_template(order)
        email_address = order["order"]["Account"]["email"]
        email_subject = 'Noshgrab Order: ' + order["order"]["id"]
        if CONFIG.version == "DEVELOPMENT":
            '''
            I had to set enviroment variables with AWS Keys for below to work.
            No hardcode.

            Because Sandbox only allows verified emails as senders/recipients we check to ensure 
            correct order+email pairing by placing the email_subject and email_adress 
            in the same string which is passed as the email subject line.
            This ensures we are sending the right order to the right email
            '''
            # email.send(email_subject + email_address, 'dev.hmsk@gmail.com')
            
            print(json.dumps(order, indent=4, default=str))
            
            with open(f'{order["order"]["id"]}_invoice.html', 'w') as f:
                f.write(html)
        
        # Uncomment below for Production usage:
        # elif CONFIG.version == "PRODUCTION":
                # email.send(email_subject, email_address)

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
            subtotal += item.gross_sales
        
        taxes = subtotal * CONFIG.info['invoice_percentage']['taxes']
        
        created_at = order.created_at
        updated_at = order.updated_at
        pickup_at = order.pickup_at
        # create new object for email use
        order_object_to_email = Order(order_id, account_id, OrderState.OPEN, subtotal, taxes,
                                    created_at, updated_at, pickup_at, items, parent_id)
        order_list.append(order_object_to_email)

    return order_list


def create_json_email(account_dict, sub_order):
    items_json_list = []
    for item in sub_order.items:
        items_json_list.append(item.to_json())

    if sub_order.account_id in account_dict:
        json_email_dict = {"order":
                           {"id": sub_order.id,
                            "Account": account_dict[sub_order.account_id].to_json(),
                            "Items": items_json_list,
                            "taxes": sub_order.taxes,
                            "sub_total": sub_order.subtotal,
                            "service_fee": sub_order.subtotal * CONFIG.info['invoice_percentage']['service_fee'],
                            "credit_card_fee": (sub_order.subtotal + sub_order.taxes) * CONFIG.info['invoice_percentage']['credit_fee'],
                            "created_at": sub_order.created_at,
                            "updated_at": sub_order.updated_at,
                            "pickup_at": sub_order.pickup_at}}

    return json_email_dict

@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'Hello World'

if __name__ == "__main__":
    with app.app_context():
        main()
        app.run()