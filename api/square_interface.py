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

            base_item_id = item['id']
            print(" ")
            print('this is the unifying id of the base item and is shared across variations')
            print(f'base item id: {base_item_id}')
            base_item_data = item['item_data']
            base_item_name = base_item_data['name']

            print(f'base item name: {base_item_name}')
            #print(f'base item data: {base_item_data}')
            base_item_variation_collection = base_item_data['variations']

            # pass into subclass
            base_variation_data = base_item_variation_collection[0]
            #print(base_variation_data)
            # print('data ok')
            base_variation_name = base_item_name + " - " + base_variation_data['type']
            print(f'base variant name: {base_variation_name}')
            base_variation_id = base_variation_data['id']
            print(f'base variation id: {base_variation_id}')

            # below is stored as boolean value (True/False).
            # AAAL = Available at all locations

            base_variation_AAAL = base_variation_data['present_at_all_locations']
            print(f'boolean value of availability: {base_variation_AAAL}')

            if base_variation_AAAL == True:
                base_variation_A = None
                base_variation_NA = None
                print("available everywhere")
            else:
                # A = Available
                base_variation_A = base_variation_data['present_at_location_ids']
                print(f'available locations: {base_variation_A}')
                # NA = Not Available
                base_variation_NA = base_variation_data['absent_at_location_ids']
                print(f'not present at locations: {base_variation_NA}')

            print(" ")

            length_of_list = len(base_item_variation_collection)
            
            '''

            for item in list, go through list and do something
            track how many items are in the list and do it for each item 
            using index location.

            we have length of list, so now we need to track how we iterate through it
            and make sure it does so correctly until it terminates at the last item
            so we don't run into going into an out of bounds index


            '''
            range_of_list = range(length_of_list)
            #print(range_of_list)

            for index_location in range(length_of_list):
                
                variation_data = self.interate_through_list(index_location, base_item_variation_collection)
                print(f'test{variation_data}')
                print(type(variation_data))


        return result

    def get_orders(self):
        pass

    def interate_through_list(self, index_location, base_item_variation_collection):

        variation_index = base_item_variation_collection[index_location]

        
        
        return variation_index
