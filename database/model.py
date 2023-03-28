import sqlalchemy.orm as orm
import enum
import datetime
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, TIMESTAMP, Integer, BigInteger
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKeyConstraint
from abc import ABC, abstractmethod

db = SQLAlchemy()

class OrderState(enum.Enum):
    OPEN = "OPEN"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"

'''
We abstract this model so all the table objects can share useful methods
'''
class AbstractModel(db.Model):
    __abstract__ = True

    # When we compare objects. Instead of comparing against memory address we can compare against the id because ids are unique
    def __eq__(self, object):
        if not object:
            return False
        return self.id == object.id
    
    # This update function will look for all public attributes and update it withe the new objects public attribute of the same name
    def update(self, updated_object):
        for attr in vars(self):
            if not attr.startswith('_'):
                updated_value = getattr(updated_object, attr)
                setattr(self, attr, updated_value)

class Account(AbstractModel):
    __tablename__ = "account"
    id = orm.mapped_column(String(30), primary_key=True)
    merchant_id: orm.Mapped[Optional[str]]
    name: orm.Mapped[str]
    email: orm.Mapped[str]
    address: orm.Mapped[str]
    locality: orm.Mapped[str]
    state: orm.Mapped[str] = orm.mapped_column(String(3))
    postal: orm.Mapped[str]
    country: orm.Mapped[str] = orm.mapped_column(String(5))

    def __init__(self, account_id, merchant_id=None, name=None, email=None, addressline1=None,
                 locality=None, state=None, postal=None, country=None):
        self.id = account_id
        self.merchant_id = merchant_id
        self.name = name
        self.email = email
        self.address = addressline1
        self.locality = locality
        self.state = state
        self.postal = postal
        self.country = country

class Order(AbstractModel):
    __tablename__ = "order"
    id = orm.mapped_column(String(50), primary_key=True)
    parent_id = orm.Mapped[str]
    account_id: orm.Mapped[str]
    state: orm.Mapped[OrderState]
    subtotal: orm.Mapped[float]
    taxes: orm.Mapped[float]
    service_fee: orm.Mapped[Optional[float]]
    credit_fee: orm.Mapped[Optional[float]]
    created_at: orm.Mapped[datetime.datetime]

    orders: orm.Mapped["OrderedItem"] = orm.relationship(back_populates="order")

    def __init__(self, order_id, account_id, state=None, subtotal=0, taxes=0,
                 service_fee=0, credit_fee=0, created_at=None, items=None, parent_id=None):
        self.id = order_id
        self.parent_id = parent_id
        self.account_id = account_id
        self.state = state
        self.subtotal = subtotal
        self.taxes = taxes
        self.service_fee = service_fee
        self.credit_fee = credit_fee
        self.created_at = created_at
        self.items = items

class Item(AbstractModel):
    __tablename__ = "item"
    id = orm.mapped_column(String(30), primary_key=True)
    version: orm.Mapped[int] = orm.mapped_column(BigInteger, primary_key=True)
    account_id: orm.Mapped[str]
    name: orm.Mapped[str]
    price: orm.Mapped[float]

    items: orm.Mapped["OrderedItem"] = orm.relationship(back_populates="item")

    def __init__(self, item_id, version, item_name, item_price, account_id):
        self.id = item_id
        self.version = version
        self.account_id = account_id
        self.name = item_name
        self.price = item_price

    def get_price(self):
        return self.price
    
    # Items overrides the __eq__ from the abstract class because it utilizes version to gaurantee uniqueness
    def __eq__(self, object):
        if not object:
            return False
        return self.id == object.id and self.version == object.version
    
class OrderedItem(AbstractModel):
    __tablename__ = "ordereditem"

    id = orm.mapped_column(Integer, primary_key=True, index=True)
    order_id: orm.Mapped[str] = orm.mapped_column(ForeignKey("order.id"))
    item_id: orm.Mapped[str]
    item_version: orm.Mapped[int] = orm.mapped_column(BigInteger)

    __table_args__ = (
            ForeignKeyConstraint(["item_id", "item_version"], [Item.id, Item.version]), {}
        )
    
    item: orm.Mapped["Item"] = orm.relationship(back_populates="items")
    order: orm.Mapped["Order"] = orm.relationship(back_populates="orders")

    def __init__(self, order_id, item_id, item_version):
        self.order_id = order_id
        self.item_id = item_id
        self.item_version = item_version
