from api.web import Square
from database.model import db
from flask import Flask
from database.managers import NoshGrab
from api.web import Square
from config.config import CONFIG
from api.email import ASes
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

    email_client = ASes(CONFIG.info['email'])
    args = {
        'TEST': 1234, 
        'OTHER': 'TESTING', 
        'NEST': {
            'NESTED': 'VALUE1',
            'LIST': [
                {
                    'id': 1
                },
                {
                    'id': 2
                }
            ]
            },
        }
    rendered = email_client.load_template('test.template', args)
    print(rendered)

    # Check for every order from Square. Check if order is in the database list of orders from database.get.orders()
    for order in orders:
        if order not in db_orders:
            print(order.id)

if __name__ == "__main__": 
    with app.app_context():
        main()