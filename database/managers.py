#!/bin/env
from .model import Account
from .model import Item
from .model import Order, OrderedItem
from functools import wraps

class NoshGrab:
    '''
    Internal Class used as a wrapper to extend select/querying functions
    For any table searches we can define the select/query function as a method in this class.
    This allows developers to call the NoshGrab Database wrapper like so: NoshGrab.get.<table>.
    '''
    class Get:
        def __init__(self, engine):
            # SQLAlchemy Engine functionality is split into attributes for easier use/access
            self.execute = engine.session.execute
            self.select = engine.select
        
        '''
        Decorator can be used here to create simple methods for simple queries by id.
        The Decorator must be called by setting the Table you want to query.
        The decorator will then run the query using that table and the provided id to search that table.
        Returns: None or Table Object
        '''
        def _select_id_compare(table):
            def decorator(func):
                @wraps(func)
                def wrapper(get_interface, _id):
                    _table = table
                    result = get_interface.execute(get_interface.select(_table).filter_by(id = _id)).scalars().first()
                    return result
                return wrapper
            return decorator

        # Item can be queried by just id or combination of id and version.
        def item(self, _id, _version=None):
            if _version:
                return self.execute(self.select(Item).filter_by(id = _id).filter_by(version = _version)).scalars().first()
            else:
                return self.execute(self.select(Item).filter(Item.id == _id)).scalars().first()
        
        # Return all items and their version variations
        def items(self):
            return self.execute(self.select(Item)).scalars().all()

        # Return ordereditem based on ordereditem id
        @_select_id_compare(OrderedItem)
        def ordereditem(self, _id):
            pass
        
        # Return account based on account id
        @_select_id_compare(Account)
        def account(self, _id):
            pass
        
        # Return order object and its items
        def order(self, _id):
            # Join is used with filter here to find the specific order based on id
            results = self.execute(self.select(Order, Item).join(Order.orders).join(Item).filter(OrderedItem.order_id ==_id)).all()
            
            if not results:
                return None
            
            '''
            Results returns a list of tuples. The first element in the tuple is the Order Object.
            The next element is the unique item from the joined table. NOTE: The Order object that is returned
            is the SAME object in every tuple.
            '''
            
            # Get the order object and initialize empty list for order.items
            order = results[0][0]
            order.items = []

            # Add all items to order
            for _order, item in results:
                order.items.append(item)

            return order
        
        # Returns list of orders and their corresponding items
        def orders(self):
            # Query for all items and join the orders with the item table
            results = self.execute(self.select(Order, Item).join(Order.orders).join(Item)).all()
            current_order = None
            orders = []

            for order, item in results:
                if order not in orders:
                    orders.append(order)

                '''
                Since this list is organized by order tuples. We can assume that when there is a 
                new order we can update current_order to be that order because the proceeding items
                in that tuple will belong to the new order. Otherwise if the order is the same as current_order
                we will append the item to the current_order.items list
                '''
                if order != current_order:
                    current_order = order
                    current_order.items = [item]
                else:
                    current_order.items.append(item)
            return orders

    '''
    Internal Class used as a wrapper to extend updating functions
    '''
    class Update:
        def __init__(self, _get, session):
            self._get = _get
            self.session = session

        '''
        This decorator runs the specific function to check if the item that should be updated exists in the database.
        If the database item is returned then we will run the Model.update function to update its attributes.
        We update the attributes because SQLAlchemy will automatically 
        '''
        def _update():
            def decorator(func):
                @wraps(func)
                def wrapper(*args, **kwargs):
                    db_item, data = func(*args, **kwargs)
                    if not db_item:
                        return False
                    else:
                        db_item.update(data)
                    
                    # The first argument here is 'self' from the wrapped function
                    _update = args[0]
                    _update.session.commit()
                    return True
                return wrapper
            return decorator
        
        '''
        The function must query the proper table for the object to update.
        This function will then return the results of the query and the data
        to update the object with
        '''
        @_update()
        def item(self, data):
            return self._get.item(data.id, data.version), data

    def __init__(self, engine):
        self.engine = engine
        self.session = self.engine.session
        self.get = self.Get(self.engine)
        self.update = self.Update(self.get, self.session)

    def add(self, data):
        '''
        If the object being added is an Order Object. We have to add the order to the database.
        Then we must add all the items from that order object. We attempt to update the item in the database.
        If the item does NOT exist we just add the item.
        As the item is added. We then add the item with its corresponding order id to the OrderedItem join table
        If the object is NOT an order object we just simply add the object
        '''
        if isinstance(data, Order):
            self.session.add(data)
            for item in data.items:
                if not self.update.item(item):
                    self.session.add(item)
                self.session.add(OrderedItem(data.id, item.id, item.version))
        else:
            self.session.add(data)
        self.session.commit()