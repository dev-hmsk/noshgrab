from square.client import Client
from database.model import Account, Item, Order
from config.config import CONFIG
from database.model import OrderState
import json
class Square:
    def __init__(self):
        self.client = None
        self.map = None

    def connect(self, token, environment='sandbox'):
        self.client = Client(
            access_token=token,
            environment=environment)

    def get_accounts(self):
        result = self.client.locations.list_locations()
        account_list = []

        if result.is_error():
            print(result.errors)
            return None
        
        for account in result.body['locations']:
            address_info = account['address']
            account_address = address_info['address_line_1']
            account_locality = address_info['locality']
            account_state = address_info['administrative_district_level_1']
            account_postal = address_info['postal_code']
            account_country = address_info['country']

            account_list.append(Account(account['id'], account['merchant_id'], account['name'], account['business_email'],
                                        account_address, account_locality, account_state, account_postal, account_country))
        return account_list

    def get_items(self):

        result = self.get_catalog(types='ITEM')

        if result.is_error():
            print(result.errors)
            return None
        
        item_object_list = []

        for item in result.body['objects']:
            base_item_data = item['item_data']
            base_item_name = base_item_data['name']
            base_item_variation_collection = base_item_data['variations']
            
            for item in base_item_variation_collection:
                item_variation_data = item['item_variation_data']
                items_variation_id = item['id']
                item_version = item['version']
                item_variation_name = item_variation_data['name']
                item_full_name = base_item_name + " " + item_variation_name
                item_option_values = item_variation_data.get('item_option_values')
                
                #Calculate Item Variation Price
                if item_variation_data.get('price_money'):
                    item_variation_price = item_variation_data['price_money']['amount']
                    # uncomment below if you require distinction of currency type
                    # item_variation_currency_type = item_variation_data['price_money']['currency']
                '''
                if item option value becomes relevant you can uncomment the below code
                '''
                # if isinstance(item_option_values, list):
                    # item_option_id = item_option_values[0]['item_option_id']
                    # item_option_value_id = item_option_values[0]['item_option_value_id']
                
                base_variation_AAAL = item['present_at_all_locations']
                
                if base_variation_AAAL == True:
                    base_variation_A = None
                    base_variation_NA = None

                else:
                    # A = Available
                    base_variation_A = item['present_at_location_ids']  
                    for account in base_variation_A:
                        if account != "LCT2A6T5GMYK0":
                            variant_item_account_id = account
                    # NA = Not Available
                    base_variation_NA = item['absent_at_location_ids']
                
                item_object = Item(items_variation_id, item_version, item_full_name,
                                   item_variation_price, variant_item_account_id)
                
                item_object_list.append(item_object)

        return item_object_list

    def get_orders(self):
        # We will query for orders from Web API based on the main account id set in config.yml
        result = self.client.orders.search_orders(body = {"location_ids": [CONFIG.info['account']['id']],"query": {"filter": {}}})
        if result.is_error():
            print(result.errors)
            return None
        
        orders = result.body['orders']
        order_object_list = []
        # pretty = json.dumps(orders, indent=4)
        # print(pretty)
        for order in orders:
            order_id = order['id']
            account_id = order['location_id']

            # Order state is set as an Enum. So we have to convert to Enum here
            state_enum = OrderState(order['state'])
            
            order_taxes = order['net_amounts']['tax_money']['amount']
            order_total = order['net_amounts']['total_money']['amount']

            order_date = order['created_at']
            updated_at = order['updated_at']
            fulfillments = order.get('fulfillments')
            line_items = order.get('line_items')
            item_object_list = []

            if line_items:
                for item in line_items:
                    item_id = item['catalog_object_id']
                    item_version = item['catalog_version']
                    quantity = int(item['quantity'])
                    item_name = item['name'] 
                    item_variation = item_name + " " + item['variation_name']
                    variant_item_account_id = self.retrieve_lineitem_account(item_id)
                    gross_sales = item['gross_sales_money']['amount']
                    base_price = item['base_price_money']['amount']
                    item_object = Item(item_id, item_version, item_variation,
                                       base_price, variant_item_account_id, gross_sales, quantity)
                    
                    item_object_list.append(item_object)

            if fulfillments:
                for details in fulfillments:
                    # pickup_details = details['pickup_details'] <- More info if required. Includes customer info, custom notes. etc.
                    pickup_at = details['pickup_details']['pickup_at']
            # This is a current workaround for orders in the test enviroment with no provided pickup_at info
            else:
                pickup_at = "0001-01-01T01:00:00.000Z"

            order_object = Order(order_id, account_id, state_enum, order_total, order_taxes,
                                    order_date, updated_at, pickup_at, item_object_list)
            
            order_object_list.append(order_object)

        return order_object_list

    def get_account_ids(self):
        '''
        this will fetch all possible accounts 
        in Square API to pass into get_accounts()
        Currently Unused. But keep in case 
        we change from hardcoding account_id
        '''
        result = self.client.locations.list_locations()

        if result.is_error():
            print(result.errors)
            return None
        
        accounts_body = result.body
        accounts = accounts_body['locations']
        account_ids = []

        for account in accounts:
            account_id = account['id']
            account_ids.append(account_id)

        return account_ids

    def get_category_id(self):
        result = self.get_catalog(types='CATEGORY')
        if result.is_error():
            print(result.errors)
            return None
        
        catalog_dict = {}

        for i in result.body['objects']:
            category_id = i['id']
            category_id_paired_name = i['category_data']['name']
            catalog_dict[category_id_paired_name] = category_id

        return catalog_dict

    def get_catalog(self, types=None):
        result = self.client.catalog.list_catalog(types=types)
        if result.is_error():
            print(result.errors)
            return None

        return result

    def retrieve_lineitem_account(self, lineitem_id):
        result = self.client.catalog.retrieve_catalog_object(
                                    object_id=lineitem_id,
                                    include_related_objects=False)
        if result.is_error():
            print(result.errors)
            return None

        accounts = result.body['object']['present_at_location_ids']

        ''' We assume that every item is set to be present_at for two accounts (Locations).
            1. The main account
            2. The account that is actually serving the item
            Therefore by removing the main account from this list. We can assume the item belongs to the remaining account (Location)
        '''
        accounts.remove(CONFIG.info['account']['id'])
        return accounts[0]
