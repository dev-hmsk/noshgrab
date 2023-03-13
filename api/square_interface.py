from square.client import Client
from database.model import Location, Address
import os

class Square:
    
    def __init__(self):
        self.client = None 
        self.map = None
    
    def connect(self, token, environment='sandbox'):
        self.client = Client(
            access_token=token,
            environment=environment)
    
    def get_locations(self):
        locations = self.client.locations.list_locations()
        locations_list = []
        catalog_dict = self.create_category_id()
        #print(catalog_dict)
        #for loop collects data from location object
        for location in locations.body['locations']:
            location_id = location['id']
            merchant_id = location['merchant_id']
            location_name = location['name']
            """
            currently the name "CHRIS'S hot chicken is mispelled to "chis's hot chicken" which 
            causes the below key verification to not correctly apply the category_id to the correct category
            specific: name in catalog api != name  in location api
            """
            if location_name in catalog_dict.keys():    
                category_id = catalog_dict[location_name]
            else:
                category_id = "PLACEHOLDER"

            location_email = location['business_email']
            address_info = location['address']
            location_address = address_info['address_line_1']
            location_locality = address_info['locality']
            location_state = address_info['administrative_district_level_1']
            location_postal = address_info['postal_code']
            location_country = address_info['country']
            #Create two Objects (address_object and location_object)
            address_object = Address(location_address, location_locality, location_state, location_postal, location_country)
            location_object = locations_list.append(Location(location_id, merchant_id, category_id, location_name, location_email, address_object))

        return locations_list
    
    def create_category_id(self):
        category = self.get_catalog('CATEGORY')
        catalog_dict = {}
        obj=category.body['objects']
        length_of_catalog = len(obj)
        for i in range(length_of_catalog):
            category_id = obj[i]['id']
            category_id_paired_name = (obj[i]['category_data']['name'])
            catalog_dict[category_id_paired_name] = category_id
        return catalog_dict
        
    def get_catalog(self,types = None):
        catalog = self.client.catalog.list_catalog(types=types)
        return catalog
    
    def get_items():
        pass

    def get_orders():
        pass