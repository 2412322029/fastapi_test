from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from sql import crud
from sql.database import get_session
from .token import get_current_user
from .verifyModel import TokenData, AdminTokenData, UserOut

adminapp = APIRouter()


async def get_admin(current_user: TokenData = Depends(get_current_user)):
    if current_user.gid == 1:
        return AdminTokenData(username=current_user.username, id=current_user.id)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='非管理员')


@adminapp.get("/test", response_model=list[UserOut | None])
async def alluserinfo(session: Session = Depends(get_session), current_admin=Depends(get_admin)):
    userlist: list[UserOut | None] = crud.get_all_user(session=session)
    return userlist
