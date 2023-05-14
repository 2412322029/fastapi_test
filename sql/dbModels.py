from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship

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

    under_posts = relationship('Post', back_populates='own_user', cascade="all, delete")  # 用户拥有的文章

    def __repr__(self):
        return f'<User>id={self.id},username={self.username},group_id={self.group_id} ...'

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

    under_posts = relationship('Post', secondary='tb_post_tag', passive_deletes=True)  # 多对多， tag被多个post拥有

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

    own_user = relationship('User', back_populates='under_posts', passive_deletes=True)  # 文章作者
    own_tags = relationship('Tag', secondary='tb_post_tag', overlaps='under_posts')  # 拥有的tag
    own_comments = relationship("Comment", back_populates="under_post", cascade="all, delete")  # 拥有的评论

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
    state = Column(Integer, nullable=False, comment='状态id', default=0)
    created_at = Column(DateTime, default=func.now(), server_default=func.now(), nullable=False, comment='创建时间')

    under_post = relationship("Post", back_populates="own_comments", passive_deletes=True)  # 所属文章

    def __repr__(self):
        return f'<Comment> id={self.id},content={self.content} ...'
