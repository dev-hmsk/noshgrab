import sqlalchemy.orm as orm
import enum
import datetime
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, TIMESTAMP, Integer
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class AccountType(enum.Enum):
    MAIN = "main"
    MERCHANT = "merchant"

class OrderState(enum.Enum):
    OPEN = "open"
    COMPLETED = "completed"
    CANCELED = "canceled"

class Account(db.Model):
    __tablename__ = "account"
    id = orm.mapped_column(String(30), primary_key=True)
    merchant_id: orm.Mapped[Optional[str]]
    type: orm.Mapped[AccountType]
    name: orm.Mapped[str]
    email: orm.Mapped[str]
    address: orm.Mapped[str]
    locality: orm.Mapped[str]
    state: orm.Mapped[str] = orm.mapped_column(String(3))
    postal: orm.Mapped[str]
    country: orm.Mapped[str] = orm.mapped_column(String(5))

    def __init__(self, account_id, merchant_id=None, type=AccountType.MERCHANT, name=None, email=None,
                 addressline1=None, locality=None, state=None, postal=None, country=None):
        self.id = account_id
        self.merchant_id = merchant_id
        self.type = type
        self.name = name
        self.email = email
        self.address = addressline1
        self.locality = locality
        self.state = state
        self.postal = postal
        self.country = country

class Order(db.Model):
    __tablename__ = "order"
    id = orm.mapped_column(String(30), primary_key=True)
    account_id: orm.Mapped[str]
    state: orm.Mapped[OrderState]
    subtotal: orm.Mapped[float]
    taxes: orm.Mapped[float]
    service_fee: orm.Mapped[Optional[float]]
    credit_fee: orm.Mapped[Optional[float]]
    created_at: orm.Mapped[datetime.datetime]

    orders: orm.Mapped["OrderedItem"] = orm.relationship(back_populates="order")

    def __init__(self, order_id, account_id, state=None, subtotal=0, taxes=0,
                 service_fee=0, credit_fee=0, created_at=None, items=None):
        self.id = order_id
        self.account_id = account_id
        self.state = state
        self.subtotal = subtotal
        self.taxes = taxes
        self.service_fee = service_fee
        self.credit_fee = credit_fee
        self.created_at = created_at
        self.items = items

class Item(db.Model):
    __tablename__ = "item"

    id = orm.mapped_column(String(30), primary_key=True)
    account_id: orm.Mapped[str]
    name: orm.Mapped[str]
    price: orm.Mapped[float]

    items: orm.Mapped["OrderedItem"] = orm.relationship(back_populates="item")

    def __init__(self, item_id, item_name, item_price, account_id):
        self.id = item_id
        self.account_id = account_id
        self.name = item_name
        self.price = item_price

    def get_price(self):
        return self.price

class OrderedItem(db.Model):
    __tablename__ = "ordereditem"
    id = orm.mapped_column(Integer, primary_key=True, index=True)
    order_id: orm.Mapped[str] = orm.mapped_column(ForeignKey("order.id"))
    item_id: orm.Mapped[str] = orm.mapped_column(ForeignKey("item.id"))

    item: orm.Mapped["Item"] = orm.relationship(back_populates="items")
    order: orm.Mapped["Order"] = orm.relationship(back_populates="orders")

    def __init__(self, order_id, item_id):
        self.order_id = order_id
        self.item_id = item_id
