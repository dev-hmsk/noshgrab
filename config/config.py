import yaml
import os

class Config:

    def __init__(self, app_version):
        self.config_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(self.config_path, 'config.yml'), 'r') as f:
            file = yaml.safe_load(f)
        self.info = file[app_version]
        self.version = app_version

CONFIG = Config(os.environ['ENVIRONMENT'])