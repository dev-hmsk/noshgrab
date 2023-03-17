from api.square_interface import Square
import os

'''

This creates a test object of Square().
Currently all funcitonality resides within Square().
Next step is to abstract by one layer and have Square()
call functions from SquareObjectMapper() instead.

'''
interface = Square()
interface.connect(os.environ['TOKEN'], environment='sandbox')

'''
Test for location and address object.
This should print all the information stored in Location()
and Address()

'''

# locations = interface.get_locations()
# for location in locations:
#     print(location)

'''
Test Code to use get_items()
This should create both the Item() and ItemVariation()
'''
# items = interface.get_items()
# print(items)

'''
Test Code to use get_orders
'''
orders = interface.get_orders()