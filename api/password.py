from fastapi import HTTPException
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from starlette import status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    try:
        flag = pwd_context.verify(plain_password, hashed_password)
        if flag:
            return True
    except UnknownHashError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='hash could not be identified')


# 加密密码
def hash_password(password):
    return pwd_context.hash(password)
