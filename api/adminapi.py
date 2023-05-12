from fastapi import APIRouter, Depends, HTTPException,Query
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from sql import crud
from sql.database import get_session
from .token import get_current_user
from .verifyModel import TokenData, AdminTokenData, UserOut
from utill.monitor import getdisk, getcpumsg
adminapp = APIRouter()

Allow_register: bool = True


def get_is_Allow_register():
    return Allow_register


limiter = Limiter(key_func=get_remote_address, enabled=True)


async def get_admin(current_user: TokenData = Depends(get_current_user)):
    if current_user.gid == 1:
        return AdminTokenData(username=current_user.username, id_=current_user.id_)
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


@adminapp.put("/review_user",
              dependencies=[Depends(get_admin)],
              summary='用户审核/封禁',
              description='gid=0正常,2审核中,3封禁')
async def review_user(uid:int=Query(default=...), group_id:crud.Ugroup=Query(default=...), session: AsyncSession = Depends(get_session)):
    await crud.review_user(session, uid, group_id)


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
async def deleteuser(username: str, session: AsyncSession = Depends(get_session), current_admin=Depends(get_admin)):
    return await crud.delete_user(session=session, username=username)

@adminapp.delete("/del_tag", summary='删除tag')
async def delTag(tag_id: int = Query(gt=0), session: AsyncSession = Depends(get_session),
                 current_admin=Depends(get_admin)):
    return await crud.del_tag(session, tag_id=tag_id)

@adminapp.get("/get_disk", summary = '获取磁盘使用情况')
async def get_disk(current_admin=Depends(get_admin)):
    return getdisk()

@adminapp.get("/get_cpu", summary = '获取cpu使用情况')
async def get_cpu(current_admin=Depends(get_admin)):
    return getcpumsg()