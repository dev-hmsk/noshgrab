from square.client import Client
import os

class Square:
    
    def __init__(self):
        self.client = None 
    
    def connect(self, token, environment='sandbox'):
        self.client = Client(
            access_token=token,
            environment=environment)
    
    def get_locations(self):
        locations = self.client.locations.list_locations()
        return locations

    def get_catalog(self,types = None):
        catalog = self.client.catalog.list_catalog(types=types)
        return catalog
