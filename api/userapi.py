import hashlib
import os

import aiofiles
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from pydantic.schema import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from config import Config
from sql import crud
from sql.database import get_session
from utill import gen
from .adminapi import get_is_Allow_register, limiter
from .token import authenticate_user, create_access_token, get_current_user
from .verifyModel import *

userapp = APIRouter()


@userapp.post("/token",
              response_model=Token,
              summary='登录返回获取token',
              description='50 pre minute')
@limiter.limit(limit_value="5/minute")
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends(),
                                 session: AsyncSession = Depends(get_session)):
    user = await authenticate_user(session=session, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.group_id == 3:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='账号被封禁,无法登录')
    access_token_expires = timedelta(minutes=int(Config['ACCESS_TOKEN_EXPIRE_MINUTES']))
    access_token = await create_access_token(
        data={"sub": user.username, "id": user.id_, 'gid': user.group_id},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@userapp.post("/register", summary='用户注册', response_model=RegisterSuccess)
@limiter.limit(limit_value="5/minute")
async def register(request: Request, user_in: UserCreate, uuid: str, code: str,
                   session: AsyncSession = Depends(get_session)):
    if get_is_Allow_register():
        b, msg = await gen.verifyCode(uu=uuid, cc=code)
        if b:
            await crud.create_user(session, user_in)
            u = await crud.findUser_by_name(session, user_in.username)
            return RegisterSuccess.from_userOut(userout=u, detail=msg + ",注册成功")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='不允许注册')


@userapp.get("/pubInfo",
             response_model=UserOut,
             summary='返回用户公开信息')
@limiter.limit(limit_value="10/minute")
async def publish_user_info(
        request: Request,
        username: str = Query(default=..., max_length=30),
        session: AsyncSession = Depends(get_session)
):
    user = await crud.findPubUser_by_name(session, username)
    if user is not None:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user:{username} not found')


@userapp.get("/info",
             response_model=UserOut,
             summary='返回当前登录用户信息')
async def userinfo(session: AsyncSession = Depends(get_session), current_user: TokenData = Depends(get_current_user)):
    user = await crud.findUser_by_name(session, current_user.username)
    if user is not None:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user:{current_user.username} not found')


@userapp.put("/update_username",
             response_model=UpdateSuccess,
             summary='更新用户名')
async def update_username(old_password: str = Query(min_length=8, max_length=200),
                          username_new: str = Query(min_length=5, max_length=30, regex=r'^[a-zA-Z0-9_ -]+$'),
                          session: AsyncSession = Depends(get_session),
                          current_user: TokenData = Depends(get_current_user)):
    r = await crud.change_user_name(session, user_old=Userbase(
        username=current_user.username,
        password=old_password), username_new=username_new)
    return r


@userapp.put("/update_password",
             response_model=UpdateSuccess,
             summary='更新密码')
async def update_password(old_password: str = Query(min_length=8, max_length=200),
                          password_new: str = Query(min_length=8, max_length=200),
                          session: AsyncSession = Depends(get_session),
                          current_user: TokenData = Depends(get_current_user)):
    r = await crud.change_user_passwd(session, user_old=Userbase(
        username=current_user.username,
        password=old_password), password_new=password_new)
    return r


@userapp.put("/update_avatar",
             response_model=UploadSuccess,
             summary='更新用户头像')
@limiter.limit(limit_value="2/minute")
async def update_avatar(request: Request, avatar_new: UploadFile, session: AsyncSession = Depends(get_session),
                        current_user: TokenData = Depends(get_current_user)):
    fileinfo = await upload(avatar_new)
    r = await crud.change_user_avatar(session, username=current_user.username, fileinfo=fileinfo)
    return r


@userapp.post("/upload_file/",
              response_model=UploadSuccess,
              dependencies=[Depends(get_current_user)],
              summary='图片文件上传')
@limiter.limit(limit_value="2/minute")
async def create_upload_file(request: Request, file: UploadFile):
    return await upload(file)


async def upload(file: UploadFile):
    ext = os.path.splitext(file.filename)[1]
    if ext not in {".jpg", ".jpeg", ".png", ".gif"}:
        raise HTTPException(status_code=400, detail="Invalid file extension.")

    data = await file.read()
    if len(data) > int(Config['MAX_FILE_SIZE_MB']) * 1048576:
        raise HTTPException(status_code=400, detail=f"File size = {round(len(data) / 1048576, 2)}MB exceeds the limit.")

    md5 = hashlib.md5(data).hexdigest()
    filename = f"{md5}{ext}"
    file_path = os.path.join(os.path.dirname(__file__), "..", "uploads", filename)
    if os.path.exists(file_path):
        return UploadSuccess(filename=filename, content_type=file.content_type, detail="文件已存在")
    async with aiofiles.open(file_path, "wb") as buffer:
        await buffer.write(data)
    return UploadSuccess(filename=filename, content_type=file.content_type, detail="上传成功")


@userapp.get("/get_code", summary='获取验证码', response_model=respCode)
@limiter.limit(limit_value="5/minute")
async def get_code(request: Request):
    base64_img, u = await gen.generateCode()
    return respCode(uuid=u, img=base64_img)


@userapp.get("/verify_code", summary='验证')
@limiter.limit(limit_value="10/minute")
async def verify_code(uuid: str, code: str, request: Request):
    b, msg = await gen.verifyCode(uu=uuid, cc=code)
    if b:
        return msg
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
