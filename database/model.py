class Account:
    def __init__(self, account_id=None,
                 merchant_id=None,
                 category_id=None,
                 account_name=None,
                 account_email=None,
                 addressline1=None,
                 locality=None,
                 state=None,
                 postal=None,
                 country=None):
        self.account_id = account_id
        self.merchant_id = merchant_id
        self.category_id = category_id
        self.name = account_name
        self.email = account_email
        self.address = addressline1
        self.locality = locality
        self.state = state
        self.postal = postal
        self.country = country

    def __repr__(self):
        info1 = (f'Name: {self.name} \n Account id: {self.account_id} \n Merchant id: {self.merchant_id} \n Category id: {self.category_id} \n email: {self.email}')
        info2 = (f'\n Physical Address: {self.address} \n Locality: {self.locality} \n State: {self.state} \n Postal: {self.postal} \n Country: {self.country}')
        info3 = info1 + info2
        return info3


class Order:
    def __init__(self,
                 order_id,
                 account_id,
                 state_enum=None,
                 subtotal=0,
                 taxes=0,
                 service_fee=0,
                 credit_fee=0,
                 date=None,
                 items=None,
                 ):
        self.order_id = order_id
        self.account_id = account_id
        self.state_enum = state_enum
        self.subtotal = subtotal
        self.taxes = taxes
        self.service_fee = service_fee
        self.credit_fee = credit_fee
        self.date = date
        self.items = items
                
    def __repr__(self):
        info1 = (f'\norder id: {self.order_id}\naccount id: {self.account_id}\nstate_enum = {self.state_enum}')
        info2 = (f'\nsub total: {self.subtotal}\ntaxes: {self.taxes}\nservice fee: {self.service_fee}\ncredit fee: {self.service_fee}')
        info3 = (f'\ncredit fee: {self.credit_fee}\ndate: {self.date}\nitems: {self.items}')
        info4 = info1 + info2 + info3
        return info4


class Item:
    def __init__(self,
                 item_id,
                 item_variation_name,
                 item_price,
                 variant_item_account_id=None
                 ):
        self.item_id = item_id
        self.variant_item_account_id = variant_item_account_id
        self.item_variation_name = item_variation_name
        self.price = item_price

    def __repr__(self):
        info1 = (f'\nItem_ID: {self.item_id}\nItem_account_ID: {self.variant_item_account_id}')
        info2 = (f'\nItem_Variation Name: {self.item_variation_name}\nItem_Variation_price: {self.price}\n')
        info3 = info1 + info2
        return info3    

    def get_price(self):
        return self.price