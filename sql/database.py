from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from config import Config

d = Config["databases"]

DATABASE_URL = f'mysql+aiomysql://{d["username"]}:{d["password"]}@{d["host"]}:{d["port"]}/{d["dbname"]}'
engine = create_async_engine(
    DATABASE_URL,
    hide_parameters=True,
    connect_args={'charset': 'utf8mb4'}
)
engine.echo = 'debug' if Config['Development'] else True
engine.echo = False

async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()


async def get_session():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


if __name__ == '__main__':
    ...
