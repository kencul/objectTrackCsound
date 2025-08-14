import sys
import os

import constants


def genYaml(path):    
    # Now process each string into the specified format
    result = [
        f"  {s}: []"
        for s in constants.CLASSES
    ]
    
    # Save to a YAML file
    with open(os.path.join(path, 'objects.yaml'), 'w') as f:
        f.write('objects:\n')
        f.write('  default: []\n')
        f.write('\n'.join(result))