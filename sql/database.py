from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from config import Config

d = Config["databases"]

DATABASE_URL = f'mysql+aiomysql://{d["username"]}:{d["password"]}@{d["host"]}:{d["port"]}/{d["dbname"]}'


async def create_db_pool():
    engine = create_async_engine(
        DATABASE_URL,
        hide_parameters=True,
        echo=False,
        connect_args={'charset': 'utf8mb4'}
    )
    return engine


async def get_session():
    engine = await create_db_pool()
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
    await engine.dispose()

if __name__ == '__main__':
    ...