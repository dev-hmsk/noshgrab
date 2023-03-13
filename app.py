from api.square_interface import Square
from database.model import Location, PhysicalAddress
import os

interface = Square()

interface.connect(os.environ['TOKEN'], environment = 'production')

category = interface.get_catalog('CATEGORY')


locations = interface.get_locations()
locations_list = []

for location in locations.body['locations']:
    location_id = location['id']
    location_name = location['name']
    location_email = location['business_email']
    address_info = location['address']
    location_address = address_info['address_line_1']
    location_locality = address_info['locality']
    location_state = address_info['administrative_district_level_1']
    location_postal = address_info['postal_code']
    location_country = address_info['country']
    physical_address = PhysicalAddress(location_address,location_locality,location_postal,location_country)

    location_object = locations_list.append(Location(location_id,location_name,location_email, physical_address))

for location in locations_list:
    print(location.name)
    print(location.physical_address.address)
