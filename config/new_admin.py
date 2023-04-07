import asyncio
import sys

sys.path.append('../')
from api.password import hash_password
from config import Config
from sql.database import get_session
from sql.dbModels import User

username = Config['Default_Administrator']
password = hash_password(Config['Default_Passwd'])


async def t():
    async for session in get_session():
        session.add(User(
            username=username,
            password=password,
            avatar='default.jpg',
            group_id=1) #0普通用户， 1管理员
        )
        await session.commit()


async def main():
    await t()

if __name__ == '__main__':

    asyncio.run(main())
