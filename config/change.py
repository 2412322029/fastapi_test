import os.path

import ruamel.yaml

yaml = ruamel.yaml.YAML()
ppath = os.path.dirname(__file__)
with open(os.path.join(ppath, 'config.yaml'), 'r', encoding='utf8') as f:
    Config: dict = yaml.load(f)


def show(arg: str = ''):
    if arg == '':
        for i, j in Config.items():
            if isinstance(j, dict):
                for k, v in j.items():
                    print(f'{i}.{k} : {v}')
            else:
                print(f'{i} : {j}')
    else:
        arg = arg.split('.')
        p1 = Config.get(arg[0])
        if len(arg) == 1:
            print(p1)
        elif len(arg) == 2:
            if isinstance(p1, dict):
                p2 = p1.get(arg[1])
                if p2 is not None:
                    print(Config[arg[0]][arg[1]])
                else:
                    print(f'not found {arg}')


def setc(arg: str, *args):
    arg = arg.split('.')
    p1 = Config.get(arg[0])
    args = list(args)
    if len(args) == 1:
        if str(args[0]).lower() == 'true':
            args[0] = True
        if str(args[0]).lower() == 'false':
            args[0] = False
    if len(arg) == 1:
        if isinstance(p1, dict):
            print(f'[{arg[0]}] is a dict, use "." ')
            print(show('.'.join(arg)))
        elif isinstance(p1, list):
            Config[arg[0]] = list(args)
            print(Config[arg[0]])
        else:
            Config[arg[0]] = args[0]
            print(Config[arg[0]])
    elif len(arg) == 2:
        if isinstance(p1, dict):
            p2 = Config.get(arg[0]).get(arg[1])
            if p2 is not None:
                Config[arg[0]][arg[1]] = args[0]
                print(Config[arg[0]][arg[1]])
            else:
                print(f'not found {arg}')
    with open(os.path.join(ppath, 'config.yaml'), "w", encoding='utf8') as fs:
        yaml.dump(Config, fs)


