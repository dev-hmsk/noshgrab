from api.web import Square
from database.model import db
from flask import Flask
from database.managers import NoshGrab
from api.web import Square
import os

app = Flask(__name__)

# Waiting for config
app.config['SQLALCHEMY_DATABASE_URI'] = ''

db.init_app(app)

def main():
    web_s = Square()
    database = NoshGrab(db)

    web_s.connect(os.environ['TOKEN'], environment='sandbox')


if __name__ == "__main__": main()