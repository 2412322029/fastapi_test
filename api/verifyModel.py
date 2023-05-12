from datetime import datetime
from typing import Optional, Type, List

from pydantic import BaseModel, Field

from sql.dbModels import User


class Userbase(BaseModel):
    username: str = Field(min_length=5, max_length=30, regex=r'^[a-zA-Z0-9_ -]+$')
    password: str = Field(min_length=8, max_length=200)


class UserCreate(Userbase):
    avatar: Optional[str] = Field(default='default.jpg')


class UserOut(BaseModel):
    id_: int
    username: str
    avatar: str
    group_id: int
    state: int
    created_at: datetime
    updated_at: datetime


class UserInDB(UserOut):
    password: str




class RegisterSuccess(BaseModel):
    detail: str
    data: UserOut

    @classmethod
    def from_userOut(cls, userout: UserOut, detail: str):
        return cls(
            detail=detail, data=userout
        )


class UpdateSuccess(RegisterSuccess):
    @classmethod
    def from_User(cls, user: Type[User], detail: str):
        return cls(
            detail=detail, data=UserOut(
                id_=user.id,
                username=user.username,
                avatar=user.avatar,
                group_id=user.group_id,
                state=user.state,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
        )


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    id_: int
    gid: int


class AdminTokenData(BaseModel):
    username: str
    id_: int


class UploadSuccess(BaseModel):
    filename: str
    content_type: str
    detail: str


class ANewTag(BaseModel):
    name: str = Field(max_length=50)


class TagInDB(BaseModel):
    name: str = Field(max_length=50)
    id_: int
    reference_count: int


class PostInDB(BaseModel):
    username: str
    title: str
    content: str
    tag_names: list[Optional[str]]


class PostIn(BaseModel):
    title: str = Field(max_length=50)
    content: str
    tag_names: list[Optional[str]]


class PostUpdate(BaseModel):
    pid: int
    title: str = Field(max_length=50)
    content: str


class PostOut(BaseModel):
    id_: int
    user_id: int
    author: str
    author_img: str
    title: str
    content: str
    tags: list[str]
    state: int
    created_at: datetime
    updated_at: datetime


class PostOutPage(BaseModel):
    page: int
    pagesize: int
    total: int
    posts: List[Optional[PostOut]]


class CommentIn(BaseModel):
    post_id: int = Field(gt=0)
    parent_id: int
    username: str
    content: str = Field(max_length=500, min_length=1)


class CommentInput(BaseModel):
    post_id: int = Field(gt=0)
    parent_id: int
    content: str = Field(max_length=500, min_length=1)


class CommentPostOut(BaseModel):
    id_: int
    post_id: int
    parent_id: int
    username: str
    user_img: str
    content: str
    reply: Optional[List['CommentPostOut']]
    created_at: datetime


class CommentUserOut(BaseModel):
    id_: int
    post_id: int
    parent_id: int
    username: str
    user_img: str
    content: str
    state: int
    created_at: datetime


class respCode(BaseModel):
    uuid: str
    img: str
