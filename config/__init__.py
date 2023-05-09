import os
import yaml

ppath = os.path.dirname(__file__).replace('config', '')
with open(os.path.join(ppath, 'config.yaml'), 'r', encoding='utf8') as f:
    Config = yaml.safe_load(f)


def options():
    import argparse
    print(f'run in {ppath}')
    parser = argparse.ArgumentParser(description='可选参数')
    parser.add_argument('-p','--port', type=int,help='set port' ,default=Config["uvicorn"]["port"])
    parser.add_argument('--vite', action='store_true',help='Also run vite' ,default=False)
    parser.add_argument('--open', action='store_true',help='Also open the browser' ,default=False)
    parser.add_argument('--dev', action='store_true',help='set Development=true', default= Config["Development"])
    args = parser.parse_args()
    Config["uvicorn"]["port"]=args.port
    Config["Development"]=args.dev
    print(args)
    if not args.vite and args.open:
        os.system(f'start chrome http://127.0.0.1:{args.port}')

    if args.vite:
        with open(f'{ppath}static/src/host.ts', 'w') as f:
            f.write(f"export const host:string = 'http://127.0.0.1:{args.port}'")
        os.system(f'start cmd /k "cd {ppath}static && npm run dev"')

def env():
    if 'MYSQL_HOST' in os.environ:
        print("use env mysql")
        Config['databases']['host'] = os.environ['MYSQL_HOST']
        Config['databases']['username'] = os.environ['MYSQL_USER']
        Config['databases']['password'] = os.environ['MYSQL_PASSWORD']
        Config['databases']['dbname'] = os.environ['MYSQL_DATABASE']

    if os.getenv('dev') == 'true':
        Config['Development'] = True
        print('Development = True')       


env()

