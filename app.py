from api.square_interface import Square
import os

interface = Square()
interface.connect(os.environ['TOKEN'], environment = 'production')
locations = interface.get_locations()

#print(locations)
#below is test prints to ensure correct attribution of information

for location in locations:
    print(repr(location))


#category = interface.get_catalog('CATEGORY')
#test= interface.create_category_id()
#print(category)