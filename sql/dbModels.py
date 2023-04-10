import sys

from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey, Text, select
from sqlalchemy.orm import declarative_base

sys.path.append('../')

Base = declarative_base()


class User(Base):
    __tablename__ = 'tb_user'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False, comment='用户名')
    password = Column(String(255), unique=False, nullable=False, comment='密码')
    avatar = Column(String(255), unique=False, nullable=True, default='', comment='头像')
    group_id = Column(Integer, unique=False, nullable=False, comment='用户组id', default=0)
    state = Column(Integer, unique=False, nullable=False, comment='状态id', default=0)
    created_at = Column(DateTime, default=func.now(), server_default=func.now(), nullable=False, comment='创建时间')
    updated_at = Column(DateTime, default=func.now(), server_default=func.now(), nullable=False, onupdate=func.now(),
                        comment='更新时间')

    # under_posts = relationship('Post', back_populates='own_user', cascade="all, delete")  # 用户拥有的文章

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


class Tag(Base):
    __tablename__ = 'tb_tag'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    reference_count = Column(Integer)

    # under_posts = relationship('Post', secondary='tb_post_tag')  # 多对多， tag被多个post拥有

    def __repr__(self):
        return f'<tag> id={self.id},name={self.name}'


class Post(Base):
    __tablename__ = 'tb_post'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("tb_user.id"), nullable=False)
    title = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    state = Column(Integer, unique=False, nullable=False, comment='状态id', default=0, server_default='0')
    created_at = Column(DateTime, default=func.now(), server_default=func.now(), nullable=False, comment='创建时间')
    updated_at = Column(DateTime, default=func.now(), server_default=func.now(), nullable=False, onupdate=func.now(),
                        comment='更新时间')

    # own_user = relationship('User', back_populates='under_posts')  # 文章作者
    # own_tags = relationship('Tag', secondary='tb_post_tag', overlaps='under_posts', cascade="all, delete")  # 拥有的tag
    # own_comments = relationship("Comment", back_populates="under_post", cascade="all, delete")  # 拥有的评论

    def __repr__(self):
        return f'<post> id={self.id},title={self.title} ...'


class PostTag(Base):  # 中间表
    __tablename__ = 'tb_post_tag'
    post_id = Column(Integer, ForeignKey("tb_post.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tb_tag.id"), primary_key=True)

    def __repr__(self):
        return f'<post_tage> post_id={self.post_id},tag_id={self.tag_id} ...'


class Comment(Base):
    __tablename__ = 'tb_comments'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('tb_post.id'), nullable=False)
    parent_id = Column(Integer, nullable=False)
    uid = Column(Integer, ForeignKey('tb_user.id'), nullable=False)
    content = Column(Text, nullable=False)
    state = Column(Integer, nullable=False, comment='状态id', default=1)
    created_at = Column(DateTime, default=func.now(), server_default=func.now(), nullable=False, comment='创建时间')

    # under_post = relationship("Post", back_populates="own_comments")  # 所属文章

    def __repr__(self):
        return f'<Comment> id={self.post_id},content={self.content} ...'



def main():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from api.password import hash_password
    from config import Config
    d = Config["databases"]
    engine = create_engine(
        f'mysql+pymysql://{d["username"]}:{d["password"]}@{d["host"]}:{d["port"]}/{d["dbname"]}',
        hide_parameters=True,
        echo=False,
        connect_args={'charset': 'utf8mb4'}
    )
    Base.metadata.create_all(engine)
    DbSession = sessionmaker(bind=engine)
    session = DbSession()
    username = Config['Default_Administrator']
    password = hash_password(Config['Default_Passwd'])
    admin = session.query(User).where(User.username == username and User.group_id == 1).first()
    if admin is None:
        print('创建管理员')
        session.add(User(
            username=username,
            password=password,
            avatar='default.jpg',
            group_id=1)  # 0 普通用户， 1 管理员
        )
        session.commit()

    if __name__ == '__main__':
        posts = session.execute(select(Post).offset(0).limit(5))
        post_list = posts.scalars().all()
        for i in post_list:
            a = session.execute(select(User).where(User.id == i.user_id)).first()
            print(a)
        # 查询文章tag
        # result = session.query(Tag.name).join(PostTag).filter(PostTag.post_id == 2).all()
        # print(result)

        # 查询该用户发布的所有文章所关联的所有标签
        # tags = session.execute(select(Tag.name)
        #                        .join(PostTag, PostTag.tag_id == Tag.id)
        #                        .join(Post, PostTag.post_id == Post.id)
        #                        .where(Post.id.in_(select(Post.id)
        #                                           .join(User).where(User.username == '2412322029')
        #                                           .subquery().select())
        #                               ).distinct())
        # tag_list = [tag[0] for tag in tags.all()]
        # print(tag_list)

        # offset = 0
        # posts = session.execute(select(Post).offset(offset).limit(5))
        # post_list = posts.scalars().all()
        # post_out_list = []
        # for post in post_list:
        #     post_out = [
        #         post.id,
        #         post.user_id,
        #         post.own_user.username,
        #         post.own_user.avatar,
        #         post.title,
        #         post.content,
        #         [tag.name for tag in post.own_tags],
        #         post.state,
        #         post.created_at,
        #         post.updated_at
        #     ]
        #     post_out_list.append(post_out)
        # print(post_out_list)


main()
