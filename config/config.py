import yaml
import os

class Config:

    def __init__(self, app_version):

        with open('config/config.yml', 'r') as f:
            file = yaml.safe_load(f)
        self.info = file[app_version]
        self.version = app_version

CONFIG = Config(os.environ['ENVIRONMENT'])