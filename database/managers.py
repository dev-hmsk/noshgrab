#!/bin/env
from .model import Account, AccountType
from .model import Item
from .model import Order, OrderedItem
from functools import wraps

class NoshGrab:
    class Get:
        def __init__(self, engine):
            self.execute = engine.session.execute
            self.select = engine.select

        def _select_id_compare(table):
            def decorator(func):
                @wraps(func)
                def wrapper(get_interface, _id):
                    _table = table
                    func()
                    result = get_interface.execute(get_interface.select(_table).where(_table.id == _id)).scalars().first()
                    return result
                return wrapper
            return decorator
        
        @_select_id_compare(Item)
        def item(self, _id):
            pass
        
        @_select_id_compare(OrderedItem)
        def ordereditem(self, _id):
            pass

        def order(self, _id):
            results = self.execute(self.select(Order, Item).join(Order.orders).join(Item).where(OrderedItem.order_id == _id)).all()
            order = results[0][0]
            order.items = []
            for order, item in results:
                order.items.append(item)
            return order
        
        def account(self, account_id, type=AccountType.MERCHANT):
            return self.execute(self.select(Account).where(Account.id == account_id and Account.type == type)).scalars().first()
        
    def __init__(self, engine):
        self.engine = engine
        self.session = self.engine.session
        self.get = self.Get(self.engine)

    def add(self, data):
        self.session.add(data)
        self.session.commit()

