import asyncio

from sqlalchemy import Column, String, Integer, DateTime, func

from .database import Base, engine


class User(Base):
    __tablename__ = 'tb_user'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False, comment='用户名')
    password = Column(String(255), unique=False, nullable=False, comment='密码')
    avatar = Column(String(255), unique=False, nullable=True, default='', comment='头像')
    group_id = Column(Integer, unique=False, nullable=False, comment='用户组id', default=0)
    state = Column(Integer, unique=False, nullable=False, comment='状态id', default=0)

    created_at = Column(DateTime, default=func.now(), nullable=False, comment='创建时间')
    updated_at = Column(DateTime, default=func.now(), nullable=False, onupdate=func.now(), comment='更新时间')

    def __repr__(self):
        return f'id={self.id},username={self.username},password={self.password},等等'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'avatar': self.avatar,
            'group_id': self.group_id,
            'state': self.state,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


# class Post(Base):
#     __tablename__ = 'tb_post'
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(create_tables())
