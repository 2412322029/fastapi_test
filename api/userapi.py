from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from pydantic.schema import timedelta
from sqlalchemy.orm import Session

from config import Config
from sql import crud
from sql.database import get_session
from .token import authenticate_user, create_access_token, get_current_user
from .verifyModel import UserCreate, RegisterSuccess, UserOut, Token, TokenData, Userbase, UpdateSuccess, PubUserInfo

userapp = APIRouter()


@userapp.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 session: Session = Depends(get_session)):
    user = await authenticate_user(session=session, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=Config['ACCESS_TOKEN_EXPIRE_MINUTES'])
    access_token = await create_access_token(
        data={"sub": user.username, "id": user.id, 'gid': user.group_id},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@userapp.post("/register", description='用户注册', response_model=RegisterSuccess)
async def register(user_in: UserCreate, session: Session = Depends(get_session)):
    await crud.create_user(session, user_in)
    u = crud.findUser_by_name(session, user_in.username)
    return RegisterSuccess.from_userOut(userout=u, detail="注册成功", )


@userapp.get("/pubInfo", response_model=PubUserInfo)
async def publish_user_info(
        username: str = Query(default=..., max_length=30),
        session: Session = Depends(get_session)
):
    user = await crud.findPubUser_by_name(session, username)
    if user is not None:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user:{username} not found')


@userapp.get("/info", response_model=UserOut)
async def userinfo(session: Session = Depends(get_session), current_user: TokenData = Depends(get_current_user)):
    user = await crud.findUser_by_name(session, current_user.username)
    if user is not None:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user:{current_user.username} not found')


@userapp.put("/update_username", response_model=UpdateSuccess)
async def update_username(old_password: str, username_new: str,
                          session: Session = Depends(get_session),
                          current_user: TokenData = Depends(get_current_user)):
    r = await crud.change_user_name(session,
                                    user_old=Userbase(username=current_user.username, password=old_password),
                                    username_new=username_new)
    return r


@userapp.put("/update_password", response_model=UpdateSuccess)
async def update_password(old_password: str, password_new: str,
                          session: Session = Depends(get_session),
                          current_user: TokenData = Depends(get_current_user)):
    r = await crud.change_user_passwd(session,
                                      user_old=Userbase(username=current_user.username, password=old_password),
                                      password_new=password_new)
    return r


@userapp.put("/update_avatar", response_model=UpdateSuccess)
async def update_username(avatar_new: str, session: Session = Depends(get_session),
                          current_user: TokenData = Depends(get_current_user)):
    r = await crud.change_user_avatar(session, username=current_user.username, new_avatar=avatar_new)
    return r
