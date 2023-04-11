import os
import yaml

with open(os.path.join(os.path.dirname(__file__), '..', 'config.yaml'), 'r', encoding='utf8') as f:
    Config = yaml.safe_load(f)


def env():
    if 'MYSQL_HOST' in os.environ:
        print("use env mysql")
        Config['databases']['host'] = os.environ['MYSQL_HOST']
        Config['databases']['username'] = os.environ['MYSQL_USER']
        Config['databases']['password'] = os.environ['MYSQL_PASSWORD']
        Config['databases']['dbname'] = os.environ['MYSQL_NAME']

    elif 'AZURE_MYSQL_HOST' in os.environ:
        print("use azure mysql")
        Config['databases']['host'] = os.environ['AZURE_MYSQL_HOST']
        Config['databases']['username'] = os.environ['AZURE_MYSQL_USER']
        Config['databases']['password'] = os.environ['AZURE_MYSQL_PASSWORD']
        Config['databases']['dbname'] = os.environ['AZURE_MYSQL_NAME']

    if os.getenv('dev') == 'true':
        Config['Development'] = True
        print('Development = True')


env()
