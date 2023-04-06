from fastapi import APIRouter, Depends, HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession
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

@adminapp.get("/admininfo",
             response_model=UserOut,
             summary='管理员信息')
async def admininfo(session: AsyncSession = Depends(get_session), current_user: TokenData = Depends(get_admin)):
    user = await crud.findUser_by_name(session, current_user.username)
    if user is not None and user.group_id==1:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user:{current_user.username} not found')

@adminapp.get("/alluser",
              response_model=list[UserOut | None],
              dependencies=[Depends(get_admin)],
              summary='查询所有用户信息',
              description='返回用户信息列表')
async def alluserinfo(session: AsyncSession = Depends(get_session)):
    userlist: list[UserOut | None] = await crud.get_all_user(session=session)
    return userlist


@adminapp.get("/is_allow_register",
              response_model=bool,
              summary='返回是否可以注册',
              description='返回是否可以注册')
async def is_allow_register():
    return Allow_register


@adminapp.get("/is_limiter",
              response_model=bool,
              summary='返回是否开启接口频率限制',
              description='返回bool ')
async def is_limiter():
    return limiter.enabled


@adminapp.put("/allow_register",
              dependencies=[Depends(get_admin)],
              summary='设置是否允许注册',
              description='输入bool')
async def allow_register(allow: bool):
    global Allow_register
    Allow_register = allow
    return '修改成功'


@adminapp.put("/set_limiter",
              dependencies=[Depends(get_admin)],
              summary='设置是否开启接口频率限制',
              description='输入bool')
async def set_limiter(allow: bool):
    limiter.enabled = allow
    if allow:
        return '开启限制'
    else:
        return '关闭限制'


@adminapp.delete("/deleteuser",
                summary = '删除用户',
                description = '根据用户名')
async def deleteuser(username, session: AsyncSession = Depends(get_session), current_admin=Depends(get_admin)):
    return await crud.delete_user(session=session, username=username)
