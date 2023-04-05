from datetime import datetime
from typing import Optional, Type

from pydantic import BaseModel, Field

from sql.dbModels import User


class Userbase(BaseModel):
    username: str = Field(min_length=5, max_length=30, regex=r'^[a-zA-Z0-9_ -]+$')
    password: str = Field(min_length=8, max_length=200)


class UserCreate(Userbase):
    avatar: Optional[str]


class UserOut(BaseModel):
    id: int
    username: str
    avatar: str
    group_id: int
    state: int
    created_at: datetime
    updated_at: datetime


class UserInDB(UserOut):
    password: str


class PubUserInfo(BaseModel):
    username: str
    avatar: str


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
                id=user.id,
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
    id: int
    gid: int


class AdminTokenData(BaseModel):
    username: str
    id: int


class UploadSuccess(BaseModel):
    filename: str
    content_type: str
    detail: str

