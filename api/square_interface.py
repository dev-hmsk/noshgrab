from square.client import Client
from database.model import Location, Address
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
            """
            currently the name "CHRIS'S hot chicken is mispelled
            to "chis's hot chicken" which
            causes the below key verification to not correctly
            apply the category_id to the correct category
            specific: name in catalog api != name  in location api
            """
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
        """
        This should populate the database with an update list of items 
        within the API.
        OPTION 1:
        It seems that the Basest Item contains the Category_id, 
        while the variation of the Basest item contains the location_id.
        Categories do not respect location (i.e. they do not care which location)
        as they are set to present_at_all_locations=True.

        Category_ID can be utilized as addtional identifier to better
        seperate sellable items within stores. This is because item_variations
        track location_ids.
        This means Category_ID's could delinetate between types of goods
        within a single store front, and still retain the specificty
        to only be sellable at certain locations
        (granted by the nested location_id present within each item_variation)
        
        OPTION 2:
        by using:
        client.catalog.list_catalog(types = "Item")
        we can completely bypass category_id + structure and directly
        acess the items themselves. This new basest type ("Item")
        contains within it the type "Item_variation". the basest item_id is given 
        first and then shared within "Item_variation" as "item_id", there is then
        futher specificity given by "item_option_value_id" after passing item_variation_data 
        (which contains its own unique item_id)

        This means that Ciabatta Bread is given id = xxxx and Ciabatta Bread small 
        is also given item_id = xxxx PLUS item_option_id
        

        
        """

        result = self.get_catalog(types='ITEM')

        if result.is_success():
            print("Get_item() Success")
            #print(result.body)
        elif result.is_error():
            print("Failure")
            #print(result.errors)

        for item in result.body['objects']:
            # print(item)
            basest_item_id = item['id']
            print('this is the unifying id of the base item')
            print(f'basest item id: {basest_item_id}')

            # we might want location available in item
            # locations_available = item['present_at_location_ids']
            # print(locations_available)

            basest_item_data = item['item_data']
            basest_item_name = basest_item_data['name']
            print(f'basest item name: {basest_item_name}')
            print(f'basest item data: {basest_item_data}')
            basest_item_variation_collection = basest_item_data['variations']
            #print(f'item variation data: {basest_item_variation_collection}')
            basest_item_variation_type = basest_item_variation_collection[0]
            #print(basest_item_variation_type)
            variation_type_data_collection = basest_item_variation_type['item_variation_data']
            #print(variation_type_data_collection)
        return result

    def get_orders():
        pass