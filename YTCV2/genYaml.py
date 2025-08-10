import sys

import constants


def main():    
    # Now process each string into the specified format
    result = [
        f"  {s}: []"
        for s in constants.CLASSES
    ]
    
    # Save to a YAML file
    with open('output.yaml', 'w') as f:
        f.write('objects:\n')
        f.write('  default: []\n')
        f.write('\n'.join(result))

if __name__ == "__main__":
    main()