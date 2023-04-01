from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from sql.database import get_session
from .gettoken import hash_password
from .verifyModel import UserIn, UserOut

userapp = APIRouter()


@userapp.get("/login")
async def user_login():
    return {}


@userapp.post("/register")
def register(user: UserIn, session: Session = Depends(get_session)):
    user.password = hash_password(user.password)
    session.add(user)
    session.commit()
    return user
