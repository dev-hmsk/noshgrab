class Location:
    def __init__(self,id=None,name=None,email=None, address=None):
        self.id = id
        self.name = name
        self.email = email
        self.physical_address = address

class PhysicalAddress:
    def __init__(self,
    addressline1 = None, 
    locality = None,
    state = None,
    postal = None,
    county= None):
        self.address = addressline1
        self.locality = locality
        self.state = state
        self.postal = postal
        self.county = county

        