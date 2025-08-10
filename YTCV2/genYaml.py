import sys

import constants


def genYaml():    
    # Now process each string into the specified format
    result = [
        f"  {s}: []"
        for s in constants.CLASSES
    ]
    
    # Save to a YAML file
    with open(constants.YAML_PATH, 'w') as f:
        f.write('objects:\n')
        f.write('  default: []\n')
        f.write('\n'.join(result))