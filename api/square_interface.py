from square.client import Client
from database.model import Location, Address, Item, ItemVariation
# import os


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
        catalog_dict = self.get_category_id()
        #print(catalog_dict)
        # for loop collects data from location object
        for location in locations.body['locations']:
            # print(location)
            location_id = location['id']
            merchant_id = location['merchant_id']
            location_name = location['name']
            category_id = catalog_dict.get(location_name)

            location_email = location['business_email']
            address_info = location['address']
            location_address = address_info['address_line_1']
            location_locality = address_info['locality']
            location_state = address_info['administrative_district_level_1']
            location_postal = address_info['postal_code']
            location_country = address_info['country']

            address_object = Address(location_address, location_locality,
                                     location_state, location_postal,
                                     location_country)
            locations_list.append(Location(location_id, merchant_id,
                                           category_id, location_name,
                                           location_email, address_object))
        return locations_list
    
    def get_category_id(self):
        result = self.get_catalog(types='CATEGORY')
        catalog_dict = {}
        for i in result.body['objects']:
            category_id = i['id']
            category_id_paired_name = i['category_data']['name']
            catalog_dict[category_id_paired_name] = category_id

        return catalog_dict
        
    def get_catalog(self, types=None):
        result = self.client.catalog.list_catalog(types=types)
        if result.is_success():
            print("Catalog List Success")
            #print(result.body)
        elif result.is_error():
            print("Catalog List Failure")
            #print(result.errors)
        return result
    
    def get_items(self):

        result = self.get_catalog(types='ITEM')

        if result.is_success():
            print("Get_item() Success")
            #print(result.body)
        elif result.is_error():
            print("Failure")
            #print(result.errors)

        for item in result.body['objects']:
            #print(item)

            base_item_id = item['id']
            print(" ")
            print('this is the unifying id of the base item and is shared across variations')
            print(f'base item id: {base_item_id}')
            base_item_data = item['item_data']
            base_item_name = base_item_data['name']

            print(f'base item name: {base_item_name}')
            #print(f'base item data: {base_item_data}')
            base_item_variation_collection = base_item_data['variations']
            #print(base_item_variation_collection)
            # pass into subclass
            base_variation_data = base_item_variation_collection[0]
            #print(base_variation_data)
            # print('data ok')
            base_variation_name = base_item_name + " - " + base_variation_data['type']
            #print(f'base variant name: {base_variation_name}')
            base_variation_id = base_variation_data['id']
            #print(f'base variation id: {base_variation_id}')

            # below is stored as boolean value (True/False).
            # AAAL = Available at all locations

            base_variation_AAAL = base_variation_data['present_at_all_locations']
            #print(f'boolean value of availability: {base_variation_AAAL}')
            
            if base_variation_AAAL == True:
                base_variation_A = None
                base_variation_NA = None
                #print("available everywhere")
            else:
                # A = Available
                base_variation_A = base_variation_data['present_at_location_ids']
                #print(f'available locations: {base_variation_A}')
                # NA = Not Available
                base_variation_NA = base_variation_data['absent_at_location_ids']
                #print(f'not present at locations: {base_variation_NA}')

            length_of_list = len(base_item_variation_collection)
            #this still contains the base variation and the sublist of variation_data
            variation_list =[]
            for index_location in range(length_of_list):
                
                variation_data = self.interate_through_list(index_location, 
                                                            base_item_variation_collection)
                variation_list.append(variation_data)
            
            variation_object = ItemVariation(base_variation_name, variation_list)
            item_object = Item(base_item_id, base_item_name, variation_object)

            print(item_object.item_variation)
        return result

    def get_orders(self):
        '''
        # orders are given with the catalog_object_id which is == the basest item_variation , id. 
        i.e. the first one that appears when looking at item variations. the next indentifier
        is variation_name which == 'name' within item_variation_data. Price of the item variation
        is given by 'price_money' and is stored by lowest currency. for USD this is == to cents.
        SO 5 dollars is represented as 500 cents.

        location_id is given within tenders[]

        its possible we can use this to determine buisness email of the location and send email
        by parsing it into get_locations() or novel funciton.

        Currently we must specify locations (at least one) during the below .search_orders()
        '''
        result = self.client.orders.search_orders(body={"location_ids": ["LCT2A6T5GMYK0",
                                                                         "LX75PZ5WEVCGG",
                                                                         "LD5F95G2D0Q5W",
                                                                         "L9F5S9KFEAECZ"]})


        orders = result.body['orders']
        length_of_orders = (len(orders))
        list_of_orders = []
        for index_location in range(length_of_orders):
            #print(orders[index_location])
            list_of_orders.append(orders[index_location])
        print(list_of_orders)
        return list_of_orders

    def interate_through_list(self, index_location, base_item_variation_collection):

        variation_index = base_item_variation_collection[index_location]
        
        return variation_index

