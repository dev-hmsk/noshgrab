class Location:
    def __init__(self,location_id=None, merchant_id=None, category_id=None, location_name=None, location_email=None, address_object=None):
        self.location_id = location_id
        self.merchant_id = merchant_id
        self.category_id = category_id
        self.name = location_name
        self.email = location_email
        #below is object
        self.physical_address = address_object

    def __repr__(self):
        info = (f'Name: {self.name} \n Location id: {self.location_id} \n Merchant id: {self.merchant_id} \n Category id: {self.category_id} \n email: {self.email} \n {self.physical_address}')
        return info
    
class Address:
    def __init__(self,
    addressline1 = None, 
    locality = None,
    state = None,
    postal = None,
    country= None):
        self.address = addressline1
        self.locality = locality
        self.state = state
        self.postal = postal
        self.country = country

    def __repr__(self):
        info = (f'Physical Address: {self.address} \n Locality: {self.locality} \n State: {self.state} \n Postal: {self.postal} \n Country: {self.country}')
        return info
class Order:
    pass

class Item:
    pass