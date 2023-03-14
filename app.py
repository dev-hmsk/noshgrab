from api.square_interface import Square
import os

interface = Square()
interface.connect(os.environ['TOKEN'], environment='production')
locations = interface.get_locations()


for location in locations:
    print(repr(location))
