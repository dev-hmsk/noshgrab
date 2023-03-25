import yaml
import os

class Config:

    def __init__(self, type):

        with open('config/config.yml', 'r') as f:
            file = yaml.safe_load(f)
        if type == 'Production':
            self.info = file['Pro_']
        else:
            self.info = file['Devel_']

CONFIG = Config(os.environ['ENVIROMENT'])