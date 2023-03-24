from square.client import Client
from database.model import Account, Item, Order



class SquareInterface:
    def __init__(self):
        self.client = None
        self.map = None

    def connect(self, token, environment='sandbox'):
        self.client = Client(
            access_token=token,
            environment=environment)

    def get_account(self):
        locations = self.client.locations.list_locations()
        account_list = []
        catalog_dict = self.get_category_id()

        for location in locations.body['locations']:
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

            account_list.append(Account(location_id, merchant_id,
                                           category_id, location_name,
                                           location_email,
                                           location_address, location_locality,
                                           location_state, location_postal, 
                                           location_country))
        return account_list

    def get_items(self):

        result = self.get_catalog(types='ITEM')

        if result.is_success():
            print("Get_item() Success")
        elif result.is_error():
            print("Failure")
        item_object_list = []

        for item in result.body['objects']:
            # base_item_id = item['id']
            base_item_data = item['item_data']
            base_item_name = base_item_data['name']
            base_item_variation_collection = base_item_data['variations']
            
            for item in base_item_variation_collection:
                item_variation_data = item['item_variation_data']
                items_variation_id = item['id']
                item_variation_name = item_variation_data['name']
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
                    # NA = Not Available
                    base_variation_NA = item['absent_at_location_ids']
                
                item_object = Item(items_variation_id, base_item_name, item_variation_name, item_variation_price)
                
                item_object_list.append(item_object)

        return item_object_list

    def get_orders(self):
        # location_ids = self.get_location_ids()

        result = self.client.orders.search_orders(body = {"location_ids": ["LX75PZ5WEVCGG"],"query": {"filter": {}}})


        orders_body = result.body
        orders = orders_body['orders']
        order_object_list = []
        for order in orders:

            order_id = order['id']
            location_id = order['location_id']
            state_enum = order['state']
            order_taxes = order['net_amounts']['tax_money']['amount']
            order_service_fee = order['net_amounts']['service_charge_money']['amount']
            order_tip = order['net_amounts']['tip_money']['amount']
            order_discount = order['net_amounts']['discount_money']['amount']
            order_total = order['net_amounts']['total_money']['amount']
            '''
            to calculate sub total we add discount and subtract all other
            fees/taxes from order_total to give resultant sub total
             '''
            order_sub_total = (order_total + order_discount) - (order_taxes + order_service_fee + order_tip)
            order_date = order['created_at']
            credit_fee = 0
            line_items = order.get('line_items')
            item_object_list = []
            if line_items:
                for item in line_items:
                    item_id = item['catalog_object_id']
                    item_name = item['name'] 
                    item_variation = item_name + " " + item['variation_name']
                    variant_item_location_id = self.retrieve_lineitem_location(item_id)
                    item_price = item['base_price_money']['amount']
                    item_object = Item(item_id, variant_item_location_id, item_variation, item_price)
                    item_object_list.append(item_object)
            order_object = Order(order_id, location_id,
                                 state_enum,
                                 order_sub_total, order_taxes,
                                 order_service_fee, credit_fee,
                                 order_date, item_object_list)
         
            order_object_list.append(order_object)
        return order_object_list

    def get_location_ids(self):
        '''
        this will fetch all possible locations 
        in Square API to pass into get_accounts()
        Currently Unused. But keep in case 
        we change from hardcoding location_id
        '''
        result = self.client.locations.list_locations()

        # if result.is_success():
        #     print(result.body)
        # elif result.is_error():
        #     print(result.errors)
        locations_body = result.body
        locations = locations_body['locations']
        location_ids = []

        for location in locations:
            location_id = location['id']
            location_ids.append(location_id)
        # print(location_ids)

        return location_ids

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

        elif result.is_error():
            print("Catalog List Failure")

        return result

    def retrieve_lineitem_location(self, lineitem_id):
        result = self.client.catalog.retrieve_catalog_object(
                                    object_id=lineitem_id,
                                    include_related_objects=False)

        accounts = result.body['object']['present_at_location_ids']
        for account in accounts:
            # currently hard code NOSHGRAB TEST ACCOUNT ID to select non nosh id and return
            if account != "LCT2A6T5GMYK0":
                return account
