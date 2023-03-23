class Account:
    def __init__(self, location_id=None,
                 merchant_id=None,
                 category_id=None,
                 location_name=None,
                 location_email=None,
                 addressline1=None,
                 locality=None,
                 state=None,
                 postal=None,
                 country=None):
        self.location_id = location_id
        self.merchant_id = merchant_id
        self.category_id = category_id
        self.name = location_name
        self.email = location_email
        self.address = addressline1
        self.locality = locality
        self.state = state
        self.postal = postal
        self.country = country

    def __repr__(self):
        info1 = (f'Name: {self.name} \n Location id: {self.location_id} \n Merchant id: {self.merchant_id} \n Category id: {self.category_id} \n email: {self.email}')
        info2 = (f'\n Physical Address: {self.address} \n Locality: {self.locality} \n State: {self.state} \n Postal: {self.postal} \n Country: {self.country}')
        info3 = info1 + info2
        return info3


class Order:
    def __init__(self,
                 order_id=None,
                 location_id=None,
                 state_enum=None,
                 subtotal=0,
                 taxes=0,
                 service_fee=0,
                 credit_fee=0,
                 date=None,
                 items=None,
                 ):
        self.order_id = order_id
        self.location_id = location_id
        self.state_enum = state_enum
        self.subtotal = subtotal
        self.taxes = taxes
        self.service_fee = service_fee
        self.credit_fee = credit_fee
        self.date = date
        self.items = items
                
    def __repr__(self):
        info1 = (f'\norder id: {self.order_id}\nlocation id: {self.location_id}\nstate_enum = {self.state_enum}')
        info2 = (f'\nsub total: {self.subtotal}\ntaxes: {self.taxes}\nservice fee: {self.service_fee}\ncredit fee: {self.service_fee}')
        info3 = (f'\ncredit fee: {self.credit_fee}\ndate: {self.date}\nitems: {self.items}')
        info4 = info1 + info2 + info3
        return info4


class Item:
    def __init__(self,
                 item_id=None,
                 item_name=None,
                 item_variation=None,
                 item_price=None
                 ):
        self.item_id = item_id
        self.item_name = item_name
        self.item_variation = item_variation
        self.price = item_price

    def __repr__(self):
        info = (f'\n Item_ID: {self.item_id}\n Item_Name: {self.item_name}\n Item_Variation: {self.item_variation}\n Item_Variation_price: {self.price}\n')
        return info    

    def get_price(self):
        return self.price

