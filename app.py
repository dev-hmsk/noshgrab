from api.square_interface import Square
import os

interface = Square()
interface.connect(os.environ['TOKEN'], environment='sandbox')

# Test for location and address object
# locations = interface.get_locations()
# for location in locations:
#     print(repr(location))

# Test for Item object
#items = interface.get_items()
# for item in items:
#     print(item["ITEM"])

#test for retrieve orders

orders = interface.get_orders()