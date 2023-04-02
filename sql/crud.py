from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from api.password import verify_password, hash_password
from api.verifyModel import UserOut, UserCreate, UserInDB, Userbase, UpdateSuccess, PubUserInfo
from sql.database import get_session
from sql.dbModels import User


async def findUser_by_name(session: Session, username: str) -> UserOut | None:
    user: User | None = session.query(User).filter(User.username == username).first()
    if user is not None:
        return UserOut(
            id=user.id,
            username=user.username,
            avatar=user.avatar,
            group_id=user.group_id,
            state=user.state,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    else:
        return None


async def findPubUser_by_name(session: Session, username: str) -> PubUserInfo | None:
    user: User | None = session.query(User).filter(User.username == username).first()
    if user is not None:
        return PubUserInfo(
            username=user.username,
            avatar=user.avatar,
        )
    else:
        return None


async def get_user(session: Session, username: str) -> UserInDB | None:
    user: User | None = session.query(User).filter(User.username == username).first()
    if user is not None:
        return UserInDB(
            id=user.id,
            username=user.username,
            password=user.password,
            avatar=user.avatar,
            group_id=user.group_id,
            state=user.state,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    else:
        return None


async def check_passwd(session: Session, username: str, password: str) -> bool:
    user: User | None = session.query(User).filter(User.username == username).first()
    if user is None:
        return False
    if verify_password(password, user.password) is True:
        return True


async def create_user(session: Session, usercreate: UserCreate):
    usercreate.password = hash_password(usercreate.password)
    try:
        session.add(User(
            username=usercreate.username,
            password=usercreate.password,
            avatar=usercreate.avatar)
        )
        session.commit()
    except IntegrityError as e:
        session.rollback()
        if "Duplicate entry" in str(e):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='用户名已经被注册')


async def change_user_name(session: Session, user_old: Userbase, username_new: str) -> UserOut:
    if check_passwd(session, user_old.username, user_old.password) is True:
        try:
            session.query(User).filter(User.username == user_old.username).update({
                'username': username_new,
                'updated_at': func.now()
            })
            session.commit()
            u = session.query(User).filter(User.username == username_new).first()
            assert u is not None
            return UpdateSuccess.from_User(u, "更新成功")
        except IntegrityError as e:
            session.rollback()
            if "Duplicate entry" in str(e):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='该用户名已经存在')
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="未知错误")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='用户名或密码错误')


async def change_user_passwd(session: Session, user_old: Userbase, password_new: str,) -> UserOut:
    if check_passwd(session, user_old.username, user_old.password) is True:
        try:
            session.query(User).filter(User.username == user_old.username).update({
                'password': hash_password(password_new),
                'updated_at': func.now()
            })
            session.commit()
            u = session.query(User).filter(User.username == user_old.username).first()
            assert u is not None
            return UpdateSuccess.from_User(u, "更新成功")
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="未知错误")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='用户名或密码错误')


async def change_user_avatar(session: Session, username: str, new_avatar: str) -> UserOut:
    try:
        session.query(User).filter(User.username == username).update({
            'avatar': new_avatar,
            'updated_at': func.now()
        })
        session.commit()
        u = await session.query(User).filter(User.username == username).first()
        assert u is not None
        return UpdateSuccess.from_User(u, "更新成功")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="未知错误")


async def get_all_user(session: Session) -> list[UserOut | None]:
    users: list = session.query(User).filter(User.group_id == 0).all()
    return [UserOut(
        id=user.id,
        username=user.username,
        avatar=user.avatar,
        group_id=user.group_id,
        state=user.state,
        created_at=user.created_at,
        updated_at=user.updated_at
    ) for user in users]


if __name__ == '__main__':
    s = next(get_session())
    print(get_all_user(s))
