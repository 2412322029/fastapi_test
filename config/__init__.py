import os
import yaml

with open(os.path.join(os.path.dirname(__file__), '..', 'config.yaml'), 'r', encoding='utf8') as f:
    Config = yaml.safe_load(f)


if __name__ == '__main__':
    Config['databases']['host'] = os.environ['AZURE_MYSQL_HOST']
    Config['databases']['username'] =os.environ['AZURE_MYSQL_USER']
    Config['databases']['password'] =os.environ['AZURE_MYSQL_PASSWORD']
    Config['databases']['dbname'] =os.environ['AZURE_MYSQL_NAME']
    print(Config)
