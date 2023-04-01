from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from config import Config

d = Config["databases"]
DATABASE_URL = f'mysql+pymysql://{d["username"]}:{d["password"]}@{d["host"]}:{d["port"]}/{d["dbname"]}'

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={'charset': 'utf8'}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=True)
Base = declarative_base()


async def get_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
