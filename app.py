from api.web import Square
from database.model import db
from flask import Flask
from database.managers import NoshGrab
from api.web import Square
from config.config import CONFIG
import os

app = Flask(__name__)

# Waiting for config
db_config = CONFIG.info['database']
app.config['SQLALCHEMY_DATABASE_URI'] = f'{db_config["dialect"]}://{db_config["user"]}:{os.environ["DB_PASS"]} \
                                            @{db_config["ip"]}:{db_config["port"]}/{db_config["name"]}'

db.init_app(app)

def main():
    web_s = Square()
    database = NoshGrab(db)
    web_s.connect(os.environ['TOKEN'], environment=CONFIG.info['square']['environment'])
    orders = web_s.get_orders()

if __name__ == "__main__": main()