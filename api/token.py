from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from api.password import verify_password
from api.verifyModel import TokenData, UserInDB
from config import Config
from sql.crud import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/token")


async def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config['SECRET_KEY'], algorithm=Config['ALGORITHM'])
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, Config['SECRET_KEY'], algorithms=[Config['ALGORITHM']])
        username: str = payload.get("sub")
        uid: str = payload.get("id")
        gid: str = payload.get("gid")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, id_=uid, gid=gid)
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data


async def authenticate_user(session, username: str, password: str) -> UserInDB | None | bool:
    user = await get_user(session, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
