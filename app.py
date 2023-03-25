from api.square_interface import SquareInterface
from config.config import CONFIG
import os

'''

This creates a test object of Square().
Currently all funcitonality resides within Square().
Next step is to abstract by one layer and have Square()
call functions from SquareObjectMapper() instead.

'''
interface = SquareInterface()
interface.connect(os.environ['TOKEN'], environment='sandbox')
'''
Test for account object
should print all attributes contained within instance

'''

# accounts = interface.get_account()
# for account in accounts:
#     print(account)

'''
Test Code to use get_items()
This should create both the Item() and ItemVariation()
'''
# items = interface.get_items()
# print(items)

'''
Test Code to use get_orders
'''
# orders = interface.get_orders()
# print(repr(orders))