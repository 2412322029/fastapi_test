from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from config import Config

d = Config["databases"]

DATABASE_URL = f'mysql+aiomysql://{d["username"]}:{d["password"]}@{d["host"]}:{d["port"]}/{d["dbname"]}'

engine = create_async_engine(
    DATABASE_URL,
    hide_parameters=True,
    connect_args={'charset': 'utf8mb4'}
)


async def get_session():
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


if __name__ == '__main__':
    ...
