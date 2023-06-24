import argparse
import datetime
import os
import os.path
import sys
import tempfile
from pprint import pprint
from config.change import show, setc
import xlwt
import ruamel.yaml
from sqlalchemy import create_engine, select
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from api.password import hash_password, verify_password
from sql.dbModels import User, Base

yaml = ruamel.yaml.YAML()
ppath = os.path.dirname(__file__)
with open(os.path.join(ppath, 'config.yaml'), 'r', encoding='utf8') as f:
    Config = yaml.load(f)

if 'MYSQL_HOST' in os.environ:
    print("use env mysql config")
    Config['databases']['host'] = os.environ['MYSQL_HOST']
    Config['databases']['username'] = os.environ['MYSQL_USER']
    Config['databases']['password'] = os.environ['MYSQL_PASSWORD']
    Config['databases']['dbname'] = os.environ['MYSQL_DATABASE']

if os.getenv('dev') == 'true':
    Config['Development'] = True
parser = argparse.ArgumentParser(description='''可选参数''')
group1 = parser.add_argument_group("tools")
group1.add_argument('-l', '--list-all', action='store_true', help='list all administrators and exit', default=False)
group1.add_argument('-t', '--tables', action='store_true', help='show all tables and exit', default=False)
group1.add_argument('-n', '--new-admin', action='store_true', help='create a administrator', default=False)
group1.add_argument('-x', '--del-admin', action='store_true', help='delete a administrator', default=False)

group2 = parser.add_argument_group("in Development")
group2.add_argument('-p', '--port', type=int, help='set port', default=Config["uvicorn"]["port"])
group2.add_argument('--vite', action='store_true', help='also run vite', default=False)
group2.add_argument('--open', action='store_true', help='also open the browser', default=False)
group2.add_argument('--dev', action='store_true', help='set Development=true', default=Config["Development"])

parser.add_argument('--config', nargs='*', help='show or set config')
args = parser.parse_args()
if args.config == []:
    show()
    sys.exit()
if args.config and len(args.config) == 1:
    show(args.config[0])
    sys.exit()
elif args.config and len(args.config) > 1:
    print(args.config[0], args.config[1:])
    setc(args.config[0], *args.config[1:])
    sys.exit()


class sync_session:
    d = Config["databases"]
    _engine = create_engine(f'mysql+pymysql://{d["username"]}:{d["password"]}@{d["host"]}:{d["port"]}')
    try:
        print(f'尝试连接mysql {d["host"]}:{d["port"]}')
        _conn = _engine.connect()
        print(f'execute CREATE DATABASE IF NOT EXISTS {d["dbname"]}')
        _conn.execute(text(f'CREATE DATABASE IF NOT EXISTS {d["dbname"]};'))
        _conn.close()
        _engine.dispose()
    except Exception as e:
        print('数据库连接失败\n', e)
        sys.exit()
    print(f'mysql连接成功')
    engine = create_engine(
        f'mysql+pymysql://{d["username"]}:{d["password"]}@{d["host"]}:{d["port"]}/{d["dbname"]}',
        echo=False,
        connect_args={'charset': 'utf8mb4'}
    )
    Base.metadata.create_all(engine)
    DbSession = sessionmaker(bind=engine)

    def __enter__(self):
        self.session = self.DbSession()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        self.engine.dispose()


class sql_tool:

    @staticmethod
    def new_admin(username, password):
        with sync_session() as session:
            admin = session.query(User).where(User.username == username and User.group_id == 1).first()
            if admin is None:
                print(f'创建管理员[{username}],密码:{password}')
                session.add(User(
                    username=username,
                    password=hash_password(password),
                    avatar='default.jpg',
                    group_id=1)  # 0 普通用户， 1 管理员
                )
                session.commit()
            else:
                print(f'管理员[{username}]已经存在')
            admin = session.query(User).where(User.username == username and User.group_id == 1).first()
            if verify_password(Config['Default_Passwd'], admin.password):
                print(f'请修改默认管理员[{admin.username}]的密码')
            else:
                print(
                    f'\t默认管理员[{admin.username}]密码已修改\t创建于:[{admin.created_at}]\t更新于:[{admin.updated_at}]\n')
        return admin

    @staticmethod
    def show_admin():
        with sync_session() as session:
            admins = session.query(User).where(User.group_id == 1).all()
            for one in admins:
                print(f'\tid:[{one.id}]\t管理员:[{one.username}]\t创建于:[{one.created_at}]\t更新于:[{one.updated_at}]')

    @staticmethod
    def del_admin(username):
        with sync_session() as session:
            try:
                r = session.execute(select(User).where(User.username == username, User.group_id == 1))
                user: User = r.scalar_one_or_none()
                own = []
                if user is not None:
                    own.append({'用户': user})
                    own.append([
                        {'post': user.under_posts},
                        {'tag': [p.own_tags for p in user.under_posts]},
                        {'comments': [p.own_comments for p in user.under_posts]}]
                    )
                    pprint(own, indent=4)
                    session.delete(user)
                    session.commit()
                    print('ok')
                else:
                    print('管理员不存在')
            except Exception as e:
                session.rollback()
                print('-' * 90)
                print(e)
                print('-' * 90)
                print('无法删除, 有外键约束')

    @staticmethod
    def getAllTables():
        from sqlalchemy import text
        with sync_session() as session:
            tables = [t[0] for t in session.execute(text('show tables')).fetchall()]
        return tables

    @staticmethod
    def to_excel():
        workbook = xlwt.Workbook(encoding='utf-8')
        with sync_session() as session:
            for table_name in sql_tool.getAllTables():
                sheet = workbook.add_sheet(f'{table_name}', cell_overwrite_ok=True)
                result = session.execute(text(f"SELECT * FROM {table_name}"))
                columns = (i[0] for i in result.cursor.description)
                for index, i in enumerate(columns):
                    sheet.write(0, index, i)
                for row_idx, row in enumerate(result):
                    for col_idx, cell_value in enumerate(row):
                        if isinstance(cell_value, datetime.datetime):
                            sheet.write(row_idx + 1, col_idx, cell_value.strftime('%Y-%m-%d %H:%M:%S'))
                        else:
                            sheet.write(row_idx + 1, col_idx, cell_value)
        temp_dir = os.path.join(tempfile.gettempdir(), 'output.xls')
        workbook.save(temp_dir)
        with open(temp_dir, mode="rb") as file_like:
            yield from file_like


if args.list_all:
    sql_tool.show_admin()
    sys.exit()
if args.tables:
    print(sql_tool.getAllTables())
    sys.exit()
if args.del_admin:
    a = input('用户名:')
    sql_tool.del_admin(a)
    sys.exit()
if args.new_admin:
    print('name.len>=5, passwd.len>=8')
    a = input('用户名:')
    b = input('密码:')
    if len(a) >= 5 and len(b) >= 8:
        sql_tool.new_admin(a, b)
    else:
        print('不合要求!!!')
    sys.exit()

Config["uvicorn"]["port"] = args.port
Config["Development"] = args.dev
if Config["Development"]:
    print(f'Running on path ["{ppath}]" in Development')
if not args.vite and args.open:
    os.system(f'start chrome http://127.0.0.1:{args.port}')

if args.vite:
    with open(f'{ppath}static/src/host.ts', 'w') as f:
        f.write(f"export const host:string = 'http://127.0.0.1:{args.port}'")
    os.system(f'start cmd /k "cd {ppath}static && npm run dev"')

sql_tool.new_admin(Config['Default_Administrator'], Config['Default_Passwd'])
