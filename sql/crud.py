from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette import status

from api.password import verify_password, hash_password
from api.verifyModel import UserOut, UserCreate, UserInDB, Userbase, UpdateSuccess, PubUserInfo, UploadSuccess
from sql.dbModels import User


async def findUser_by_name(session: AsyncSession, username: str) -> UserOut | None:
    r = await session.execute(select(User).where(User.username == username))
    user: User | None = r.scalar_one_or_none()
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


async def findPubUser_by_name(session: AsyncSession, username: str) -> PubUserInfo | None:
    r = await session.execute(select(User).where(User.username == username))
    user: User | None = r.scalar_one_or_none()
    if user is not None:
        return PubUserInfo(
            username=user.username,
            avatar=user.avatar,
        )
    else:
        return None


async def get_user(session: AsyncSession, username: str) -> UserInDB | None:
    r = await session.execute(select(User).where(User.username == username))
    user: User | None = r.scalar_one_or_none()
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


async def check_passwd(session: AsyncSession, username: str, password: str) -> bool:
    r = await session.execute(select(User).where(User.username == username))
    user: User | None = r.scalar_one_or_none()
    if user is None:
        return False
    if verify_password(password, user.password) is True:
        return True


async def create_user(session: AsyncSession, usercreate: UserCreate):
    usercreate.password = hash_password(usercreate.password)
    try:
        session.add(User(
            username=usercreate.username,
            password=usercreate.password,
            avatar='default.jpg')
        )
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        if "Duplicate entry" in str(e):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='用户名已经被注册')


async def change_user_name(session: AsyncSession, user_old: Userbase, username_new: str) -> UserOut:
    if check_passwd(session, user_old.username, user_old.password) is True:
        try:
            r = await session.execute(select(User).where(User.username == user_old.username))
            user = r.scalars().first()
            if user:
                user.username = username_new
                user.updated_at = func.now()
                await session.commit()
            u = (await session.execute(select(User).where(User.username == username_new))).first()
            assert u is not None
            return UpdateSuccess.from_User(u, "更新成功")
        except IntegrityError as e:
            await session.rollback()
            if "Duplicate entry" in str(e):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='该用户名已经存在')
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="未知错误" + str(e))
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='用户名或密码错误')


async def change_user_passwd(session: AsyncSession, user_old: Userbase, password_new: str, ) -> UserOut:
    if check_passwd(session, user_old.username, user_old.password) is True:
        try:
            r = await session.execute(select(User).where(User.username == user_old.username))
            user = r.scalars().first()
            if user:
                user.password = hash_password(password_new)
                user.updated_at = func.now()
                await session.commit()
            u = (await session.execute(select(User).where(User.username == user_old.username))).first()
            assert u is not None
            return UpdateSuccess.from_User(u, "更新成功")
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="未知错误" + str(e))
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='用户名或密码错误')


async def change_user_avatar(session: AsyncSession, username: str, fileinfo: UploadSuccess) -> UploadSuccess:
    try:
        r = await session.execute(select(User).where(User.username == username))
        user = r.scalars().first()
        if user:
            user.avatar = fileinfo.filename
            user.updated_at = func.now()
            await session.commit()
        return UploadSuccess(filename=fileinfo.filename, content_type=fileinfo.content_type, detail=fileinfo.detail)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="未知错误" + str(e))


async def get_all_user(session: AsyncSession) -> list[UserOut | None]:
    r = await session.execute(select(User).where(User.group_id == 0))
    users = r.scalars().all()
    return [UserOut(
        id=user.id,
        username=user.username,
        avatar=user.avatar,
        group_id=user.group_id,
        state=user.state,
        created_at=user.created_at,
        updated_at=user.updated_at
    ) for user in users]


async def delete_user(session: AsyncSession, username: str):
    try:
        r = await session.execute(select(User).where(User.username == username))
        user = r.scalars().first()
        if user is not None:
            await session.delete(user)
            await session.commit()
            return {"detail": "删除成功"}
        else:
            return {"detail": "用户不存在，删除失败"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='未知错误' + str(e))


if __name__ == '__main__':
    ...
