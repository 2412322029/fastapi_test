import os
import yaml

with open(os.path.join(os.path.dirname(__file__), '..', 'config.yaml'), 'r', encoding='utf8') as f:
    Config = yaml.safe_load(f)

if __name__ == '__main__':
    print(Config)