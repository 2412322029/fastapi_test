from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserIn(BaseModel):
    username: str = Field(min_length=5, max_length=20, regex=r'^[a-zA-Z0-9_ -]+$')
    password: str = Field(min_length=8, max_length=20)
    avatar: Optional[str]


class UserOut(BaseModel):
    id: int
    username: str
    password: str
    avatar: str
    group_id: int
    state: int
    created_at: datetime
    updated_at: datetime
