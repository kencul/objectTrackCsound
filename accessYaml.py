import yaml
from pathlib import Path
import constants

'''
This module provides a class to access and manipulate the YAML file used to assign Csound instrument numbers to COCO objects.
'''

class AccessYaml:
    def __init__(self, directory = ''):
        self.yaml_file = directory / constants.YAML_PATH if directory else Path(constants.YAML_PATH)
        with open(self.yaml_file, 'r') as f:
            self.data = yaml.safe_load(f)
    
    def access_data(self, key):
        '''Access the data for a given key in the YAML file.
        If the value is an empty list, it returns the default value instead.
        If value is None or default value is also None, returns None.
        '''
        value = self.data['objects'].get(key, None)
            
        if value == []:
            value = self.data['objects'].get('default', None)
        
        if value == []
            value = None
            
        print(f"'{key}': {value}")
        return value