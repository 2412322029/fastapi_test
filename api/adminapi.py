from fastapi import APIRouter, Depends, HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session
from starlette import status

from sql import crud
from sql.database import get_session
from .token import get_current_user
from .verifyModel import TokenData, AdminTokenData, UserOut

adminapp = APIRouter()

Allow_register: bool = True


def get_is_Allow_register():
    return Allow_register


limiter = Limiter(key_func=get_remote_address, enabled=True)


async def get_admin(current_user: TokenData = Depends(get_current_user)):
    if current_user.gid == 1:
        return AdminTokenData(username=current_user.username, id=current_user.id)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='非管理员')


@adminapp.get("/alluser", response_model=list[UserOut | None], dependencies=[Depends(get_admin)])
async def alluserinfo(session: Session = Depends(get_session)):
    userlist: list[UserOut | None] = await crud.get_all_user(session=session)
    return userlist


@adminapp.get("/is_allow_register", response_model=bool)
async def is_allow_register():
    return Allow_register


@adminapp.get("/is_limiter", response_model=bool)
async def is_limiter():
    return limiter.enabled


@adminapp.put("/allow_register", dependencies=[Depends(get_admin)])
async def allow_register(allow: bool):
    global Allow_register
    Allow_register = allow
    return '修改成功'


@adminapp.put("/set_limiter", dependencies=[Depends(get_admin)])
async def set_limiter(allow: bool):
    limiter.enabled = allow
    if allow:
        return '开启限制'
    else:
        return '关闭限制'


@adminapp.delete("/deleteuser")
async def deleteuser(username, session: Session = Depends(get_session), current_admin=Depends(get_admin)):
    return await crud.delete_user(session=session, username=username)
