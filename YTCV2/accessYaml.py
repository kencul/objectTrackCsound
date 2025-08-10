import yaml
from pathlib import Path

yaml_file = Path('output.yaml')
with open(yaml_file, 'r') as f:
    data = yaml.safe_load(f)
    
print(data['objects']['person'])