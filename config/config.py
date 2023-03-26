import yaml
import os

class Config:

    def __init__(self, type):

        with open('config/config.yml', 'r') as f:
            file = yaml.safe_load(f)
        self.info = file[type]


CONFIG = Config(os.environ['ENVIRONMENT'])