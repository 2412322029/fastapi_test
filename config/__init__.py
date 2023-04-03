import logging
import os
import yaml

with open(os.path.join(os.path.dirname(__file__), '..', 'config.yaml'), 'r', encoding='utf8') as f:
    Config = yaml.safe_load(f)

if Config['Development'] is False:
    logging.basicConfig()
    handler = logging.FileHandler('./log/sqlalchemy.log')
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter('%(levelname)s [%(asctime)s] - %(name)s - %(message)s'))
    logging.getLogger('sqlalchemy.engine').addHandler(handler)

if __name__ == '__main__':
    print(Config)
