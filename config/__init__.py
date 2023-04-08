import os
import yaml

with open(os.path.join(os.path.dirname(__file__), '..', 'config.yaml'), 'r', encoding='utf8') as f:
    Config = yaml.safe_load(f)


def az():
    if 'AZURE_MYSQL_HOST' in os.environ.keys():
        print("使用azure mysql")
        Config['databases']['host'] = os.environ['AZURE_MYSQL_HOST']
        Config['databases']['username'] =os.environ['AZURE_MYSQL_USER']
        Config['databases']['password'] =os.environ['AZURE_MYSQL_PASSWORD']
        Config['databases']['dbname'] =os.environ['AZURE_MYSQL_NAME']
    else:
        print("使用默认数据库配置")


az()
