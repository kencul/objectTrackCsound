import yaml
from pathlib import Path
import constants

class AccessYaml:
    def __init__(self, directory = ''):
        self.yaml_file = directory / constants.YAML_PATH if directory else Path(constants.YAML_PATH)
        with open(self.yaml_file, 'r') as f:
            self.data = yaml.safe_load(f)
    
    def access_data(self, key):
        value = self.data['objects'].get(key, None)
        # if value is None:
        #     print(f"Key '{key}' not found in YAML file.")
            
        if value == []:
            #print(f"Key '{key}' has an empty list. Using default value.")
            value = self.data['objects'].get('default', None)
            
        print(f"Accessed key '{key}': {value}")
        return value