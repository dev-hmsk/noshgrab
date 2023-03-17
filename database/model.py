class Location:
    def __init__(self, location_id=None,
                 merchant_id=None,
                 category_id=None,
                 location_name=None,
                 location_email=None,
                 address_object=None):
        self.location_id = location_id
        self.merchant_id = merchant_id
        self.category_id = category_id
        self.name = location_name
        self.email = location_email
        # below is object
        self.physical_address = address_object

    def __repr__(self):
        info = (f'Name: {self.name} \n Location id: {self.location_id} \n Merchant id: {self.merchant_id} \n Category id: {self.category_id} \n email: {self.email} \n {self.physical_address}')
        return info


class Address:
    def __init__(self, 
                 location_id=None,
                 addressline1=None,
                 locality=None,
                 state=None,
                 postal=None,
                 country=None):
        self.id = location_id
        self.address = addressline1
        self.locality = locality
        self.state = state
        self.postal = postal
        self.country = country
    
    def __repr__(self):
        info = (f'Paired Location ID: {self.id} \n Physical Address: {self.address} \n Locality: {self.locality} \n State: {self.state} \n Postal: {self.postal} \n Country: {self.country}')
        return info


class Order:
    def __init__(self,
                 order_id=None,
                 location_id=None,
                 state_enum=None,
                 subtotal=None,
                 taxes=None,
                 service_fee=None,
                 credit_fee=None,
                 date=None,
                 items=None
                 ):
        self.order_id = order_id
        self.location_id = location_id
        self.state_enum = state_enum
        self.subtotal = subtotal
        self.taxes = taxes
        self.service_fee = service_fee
        self.credit_fee = credit_fee
        self.date = date
        
        self.items = Item(
                 item_id=None,
                 item_name=None,
                 item_variation=None,
                 item_price=None)
        pass


class Item:
    def __init__(self,
                 item_id=None,
                 item_name=None,
                 item_variation=None,
                 item_price=None
                 ):
        self.item_id = item_id
        self.item_name = item_name
        # make below a subclass
        self.item_variation = item_variation
        # this should be in subclass as well
        self.price = item_price

    def __repr__(self):
        info = (f'Item_ID: {self.item_id}\n Item_Name: {self.item_name}\n Item_Variation: {self.item_variation}\n Item_Variation_price: {self.price}\n')
        return info    

    def get_price(self):
        return self.price


class ItemVariation:
    #stores every possible item variation as a list
    def __init__(self,
                 variation_item_name,
                 variation_list):
        self.variation_name = variation_item_name
        self.variation_data = variation_list
        
    def __repr__(self):
        info = (f'ItemVariation(): {self.variation_data} \n Variation Name: {self.variation_name}')
        return info
