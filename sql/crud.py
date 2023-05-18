from enum import Enum

from fastapi import HTTPException
from sqlalchemy import delete, and_, desc, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.password import verify_password, hash_password
from api.verifyModel import *
from sql.dbModels import *


class Ugroup(Enum):
    normal = 0
    administrators = 1
    in_review = 2
    ban = 3


async def findUser_by_name(session: AsyncSession, username: str) -> UserOut | None:
    r = await session.execute(select(User).where(User.username == username))
    user: User | None = r.scalar_one_or_none()
    if user is not None:
        return UserOut(
            id_=user.id,
            username=user.username,
            avatar=user.avatar,
            group_id=user.group_id,
            state=user.state,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    else:
        return None


async def findPubUser_by_name(session: AsyncSession, username: str) -> UserOut | None:
    r = await session.execute(select(User).where(User.username == username))
    user: User | None = r.scalar_one_or_none()
    if user is not None:
        return UserOut(
            id_=user.id,
            username=user.username,
            avatar=user.avatar,
            group_id=user.group_id,
            state=user.state,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    else:
        return None


async def get_user(session: AsyncSession, username: str) -> UserInDB | None:
    r = await session.execute(select(User).where(User.username == username))
    user: User | None = r.scalar_one_or_none()
    if user is not None:
        return UserInDB(
            id_=user.id,
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
            group_id=Ugroup.in_review.value,
            avatar='default.jpg')
        )
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        if "Duplicate entry" in str(e):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='用户名已经被注册')


async def change_user_name(session: AsyncSession, user_old: Userbase, username_new: str) -> UserOut:
    if await check_passwd(session, user_old.username, user_old.password) is True:
        try:
            r = await session.execute(select(User).where(User.username == user_old.username))
            user = r.scalar_one_or_none()
            if user:
                user.username = username_new
                user.updated_at = func.now()
                await session.commit()
            u = (await session.execute(select(User).where(User.username == username_new))).scalar_one_or_none()
            assert u is not None
            return UpdateSuccess.from_User(u, "更新成功")
        except IntegrityError as e:
            await session.rollback()
            if "Duplicate entry" in str(e):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='该用户名已经存在')
        except Exception as e:
            await session.rollback()
            # raise e
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="未知错误" + str(e))
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='用户名或密码错误')


async def change_user_passwd(session: AsyncSession, user_old: Userbase, password_new: str, ) -> UserOut:
    if await check_passwd(session, user_old.username, user_old.password) is True:
        try:
            r = await session.execute(select(User).where(User.username == user_old.username))
            user = r.scalar_one_or_none()
            if verify_password(password_new, user.password):
                return UpdateSuccess.from_User(user, "和原密码一致，不用修改")
            if user:
                user.password = hash_password(password_new)
                user.updated_at = func.now()
                await session.commit()
            u = (await session.execute(select(User).where(User.username == user_old.username))).scalar_one_or_none()
            assert u is not None
            return UpdateSuccess.from_User(u, "更新成功")
        except Exception as e:
            await session.rollback()
            # raise e
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="未知错误" + str(e))
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='用户名或密码错误')


async def change_user_avatar(session: AsyncSession, username: str, fileinfo: UploadSuccess) -> UploadSuccess:
    try:
        r = await session.execute(select(User).where(User.username == username))
        user = r.scalar_one_or_none()
        if user:
            user.avatar = fileinfo.filename
            user.updated_at = func.now()
            await session.commit()
        return UploadSuccess(filename=fileinfo.filename, content_type=fileinfo.content_type, detail=fileinfo.detail)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="未知错误" + str(e))


async def get_all_user(session: AsyncSession) -> list[UserOut | None]:
    r = await session.execute(select(User))
    users = r.scalars().all()
    return [UserOut(
        id_=user.id,
        username=user.username,
        avatar=user.avatar,
        group_id=user.group_id,
        state=user.state,
        created_at=user.created_at,
        updated_at=user.updated_at
    ) for user in users]


async def review_user(session: AsyncSession, uid: int, group_id: Ugroup):
    try:
        r = await session.execute(select(User).where(User.id == uid))
        user = r.scalar_one_or_none()
        if user.group_id == Ugroup.administrators.value:
            return '不可更改管理员状态'
        if user:
            user.group_id = group_id
            user.updated_at = func.now()
            await session.commit()
        return '更新成功'
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="未知错误" + str(e))


async def delete_user(session: AsyncSession, username: str):
    try:
        r = await session.execute(select(User).where(User.username == username))
        user: User = r.scalar_one_or_none()
        if user is not None:
            # 删除该用户相关的所有文章的PostTag映射
            await session.execute(
                delete(PostTag).where(PostTag.post_id.in_(
                    select(Post.id).where(Post.user_id == user.id)
                ))
            )
            await updateTagCount(session)
            # TODO:先删除相关评论，解除外键约束
            p_list = (await session.execute(select(Post).where(Post.user_id == user.id))).scalars().all()
            for p in p_list:
                await delete_post(session, p.id, username)
            # 删除该用户相关的所有文章
            await session.execute(delete(Post).where(Post.user_id == user.id))
            await session.delete(user)
            await session.commit()
            return {"detail": "删除成功"}
        else:
            return {"detail": "用户不存在，删除失败"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='未知错误' + str(e))


# -------------------------------------------------------------------post
async def updateTagCount(session: AsyncSession):
    try:
        tags = await session.execute(select(Tag))
        tags = tags.all()
        for tag in tags:
            tag_id: int = tag[0].id
            count = await session.execute(select(PostTag).where(PostTag.tag_id == tag_id))
            count = len(count.all())
            tag = (await session.execute(select(Tag).where(Tag.id == tag_id))).scalar_one()
            tag.reference_count = count
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='更新tag计数失败' + str(e))


async def new_post(session: AsyncSession, a_post: PostInDB) -> PostOut:
    try:
        # 查询指定用户名的用户
        user = await session.execute(select(User).where(User.username == a_post.username))
        user = user.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=404, detail="your username not found, cannot new post")
        if user.group_id == Ugroup.in_review.value:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='账号正在审核,无法发表')
        if user.group_id == Ugroup.ban.value:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='账号被封禁,无法发表')
        # 创建新的文章
        post = Post(title=a_post.title, content=a_post.content, user_id=user.id)
        session.add(post)
        await session.commit()
        if a_post.tag_names is not []:
            tags = []
            for tag_name in a_post.tag_names:
                tag = await session.execute(select(Tag).where(Tag.name == tag_name))
                tag = tag.scalar_one_or_none()
                if tag is None:
                    tag = Tag(name=tag_name)
                    session.add(tag)
                tags.append(tag)
            # 将标签和文章关联起来
            await session.commit()
            for tag in tags:
                post_tag = PostTag(post_id=post.id, tag_id=tag.id)
                session.add(post_tag)
            await session.commit()
        await updateTagCount(session)
        return await get_post_ById(session, post.id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        await session.rollback()
        # raise e
        raise HTTPException(status_code=400, detail=str(e))


async def get_post_ById(session: AsyncSession, post_id: int) -> Optional[PostOut]:
    post = await session.execute(select(Post).where(Post.id == post_id))
    post = post.scalar_one_or_none()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    user = await get_post_owner(session, post.user_id)
    post_out = PostOut(
        id_=post.id,
        user_id=post.user_id,
        author=user.username,
        author_img=user.avatar,
        title=post.title,
        content=post.content,
        tags=await get_post_tag(session, post.id),
        state=post.state,
        created_at=post.created_at,
        updated_at=post.updated_at,
    )
    return post_out


async def get_post_tag(session: AsyncSession, pid: int) -> list[Optional[str]]:
    a = await session.execute(select(Tag.name).join(PostTag).filter(PostTag.post_id == pid))
    return [tag[0] for tag in a.all()]


async def get_post_owner(session: AsyncSession, uid: int) -> User:
    u = await session.execute(select(User).where(User.id == uid))
    return u.scalar_one_or_none()


async def get_all_posts_ByPage(session: AsyncSession, page: int, pagesize: int) -> PostOutPage:
    try:
        offset = (page - 1) * pagesize
        posts = await session.execute(select(Post).order_by(desc(Post.updated_at)).offset(offset).limit(pagesize))
        total = (await session.execute(func.count(Post.id))).scalars().all()[0]
        post_list = posts.scalars().all()
        if post_list is None:
            return PostOutPage(page=page, pagesize=pagesize, total=total, posts=[])
        post_out_list = []
        for post in post_list:
            user = await get_post_owner(session, post.user_id)
            post_out = PostOut(
                id_=post.id,
                user_id=post.user_id,
                author=user.username,
                author_img=user.avatar,
                title=post.title,
                content=str(post.content)[:200],
                tags=await get_post_tag(session, post.id),
                state=post.state,
                created_at=post.created_at,
                updated_at=post.updated_at,
            )
            post_out_list.append(post_out)
        return PostOutPage(page=page, pagesize=pagesize, total=total, posts=post_out_list)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def get_user_posts_ByPage(session: AsyncSession, username: str, page: int, pagesize: int) -> PostOutPage:
    offset = (page - 1) * pagesize
    user = await get_user(session, username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user not found')
    posts = await session.execute(select(Post).
                                  where(Post.user_id == user.id_)
                                  .order_by(desc(Post.updated_at))
                                  .offset(offset).limit(pagesize))
    post_list = posts.scalars().all()
    total = len((await session.execute(select(Post.id).filter(Post.user_id == user.id_))).scalars().all())
    post_out_list = []
    for post in post_list:
        user = await get_post_owner(session, post.user_id)
        post_out = PostOut(
            id_=post.id,
            user_id=post.user_id,
            author=user.username,
            author_img=user.avatar,
            title=post.title,
            content=str(post.content)[:200],
            tags=await get_post_tag(session, post.id),
            state=post.state,
            created_at=post.created_at,
            updated_at=post.updated_at,
        )
        post_out_list.append(post_out)
    return PostOutPage(page=page, pagesize=pagesize, total=total, posts=post_out_list)


async def get_user_all_tags(session: AsyncSession, username: str):
    tags = (await session.execute(select(Tag)
                                  .join(PostTag, PostTag.tag_id == Tag.id)
                                  .join(Post, PostTag.post_id == Post.id)
                                  .order_by(desc(Tag.reference_count))
                                  .where(Post.id.in_(select(Post.id)
                                                     .join(User).where(User.username == username)
                                                     .subquery().select())
                                         ).distinct())).all()
    tag_list = [TagInDB(id_=tag[0].id, name=tag[0].name, reference_count=tag[0].reference_count) for tag in tags]
    return tag_list


async def update_post_authorized(session: AsyncSession, post_id: int, title: str, content: str, username: str) -> str:
    try:
        post = await session.execute(select(Post).where(Post.id == post_id))
        post = post.scalar_one_or_none()
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        uid: int = post.user_id
        user = await session.execute(select(User.username).where(User.id == uid))
        user = user.scalar_one_or_none()
        if user.group_id == Ugroup.in_review.value:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='账号正在审核,无法发表')
        if user.group_id == Ugroup.ban.value:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='账号被封禁,无法发表')
        if user.username != username:
            raise HTTPException(status_code=403,
                                detail=f"You are not authorized to update, this post belong to {user.username}")
        post.title = title
        post.content = content
        post.updated_at = func.now()
        await session.commit()
        return '更新成功'
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        await session.rollback()
        # raise e
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='更新post失败,' + str(e))


async def delete_post(session: AsyncSession, post_id: int, username: str) -> str:
    try:
        post = await session.execute(select(Post).where(Post.id == post_id))
        post = post.scalar_one_or_none()
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        user = await get_user(session, username)
        if user.id_ != post.user_id:
            raise HTTPException(status_code=401, detail=f"You are not authorized to delete this post,"
                                                        f" this post belong to {user.username}")
        # 删除对应postTag
        await session.execute(delete(PostTag).where(PostTag.post_id == post_id))
        await updateTagCount(session)
        # TODO: 删除对应评论
        coms = (await session.execute(select(Comment).where(Comment.post_id == post.id))).scalars().all()
        for com in coms:
            await session.delete(com)
        await session.delete(post)
        await session.commit()
        return '删除成功'
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='删除post失败,' + str(e))


async def new_tag(session: AsyncSession, a_tag: ANewTag):
    try:
        tag = await session.execute(select(Tag).where(Tag.name == a_tag.name))
        tag = tag.first()
        if tag is not None:
            raise HTTPException(status_code=400, detail='tag已存在')
        tag = Tag(name=a_tag.name, reference_count=0)
        session.add(tag)
        await session.commit()
        return '新建成功'
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        await session.rollback()
        # raise e
        raise HTTPException(status_code=400, detail=str(e))


async def del_tag(session: AsyncSession, tag_id: int):
    try:
        await updateTagCount(session)
        t = await session.execute(select(Tag).where(Tag.id == tag_id))
        t = t.scalar_one_or_none()
        if t is None:
            raise HTTPException(status_code=404, detail='tag not found')
        if t.reference_count > 0:
            raise HTTPException(status_code=400, detail=f'have {t.reference_count} post used this tag, cannot del')
        await session.execute(delete(Tag).where(Tag.id == tag_id))
        await session.commit()
        return '删除成功'
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        await session.rollback()
        # raise e
        raise HTTPException(status_code=400, detail=str('删除失败'))


async def get_all_tags(session: AsyncSession):
    try:
        await updateTagCount(session)
        tags = await session.execute(select(Tag).order_by(desc(Tag.reference_count)))
        tags = tags.scalars().all()
        return [TagInDB(id_=tag.id, name=tag.name, reference_count=tag.reference_count) for tag in tags]
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


async def add_tag_to_post_authorized(session: AsyncSession, post_id: int, tag_name: str,
                                     username: str) -> str:
    try:
        post = await session.execute(select(Post).where(Post.id == post_id))
        post = post.scalar_one_or_none()
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        user = await get_user(session, username)
        if user.id_ != post.user_id:
            raise HTTPException(status_code=401, detail=f"You are not authorized,"
                                                        f" this post belong to {user.username}")
        tag = await session.execute(select(Tag).where(Tag.name == tag_name))
        tag = tag.scalar_one_or_none()
        if tag is None:
            tag = Tag(name=tag_name)
            session.add(tag)
        await session.commit()
        post_tag = PostTag(post_id=post.id, tag_id=tag.id)
        session.add(post_tag)
        await session.commit()
        await updateTagCount(session)
        return '更新成功'
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='更新失败' + str(e))


async def get_posts_ByTagPage(session: AsyncSession, tag_name: str, page: int, pagesize: int) -> PostOutPage:
    offset = (page - 1) * pagesize
    posts = await session.execute(select(Post).join(PostTag).join(Tag)
                                  .filter(Tag.name == tag_name).offset(offset).limit(pagesize))
    posts = posts.scalars()
    count = (await session.execute(select(Post).join(PostTag).join(Tag)
                                   .filter(Tag.name == tag_name))).all().__len__()
    post_out_list = []
    for post in posts:
        po = await get_post_ById(session, post_id=post.id)
        po.content = str(po.content)[:200]
        post_out_list.append(po)
    return PostOutPage(page=page, pagesize=pagesize, total=count, posts=post_out_list)


async def newComment(session: AsyncSession, cin: CommentIn) -> str:
    try:
        user = await findUser_by_name(session, cin.username)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户id不存在,无法发表')
        if user.group_id == Ugroup.in_review.value:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='账号正在审核,无法发表')
        if user.group_id == Ugroup.ban.value:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='账号被封禁,无法发表')
        post = await session.execute(select(Post).where(Post.id == cin.post_id))
        post = post.scalar_one_or_none()
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='文章不存在,无法发表')
        if int(cin.parent_id) != 0:  # 不是顶层评论
            p_comm = await session.execute(select(Comment).where(Comment.id == cin.parent_id))
            p_comm = p_comm.scalar_one_or_none()
            if p_comm is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='回复的评论不存在,无法发表')
            if p_comm.state == 0:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='回复的评论正在审核,无法发表')
        comm = Comment(
            post_id=cin.post_id,
            parent_id=cin.parent_id,
            uid=user.id_,
            content=cin.content,
            created_at=func.now(),
        )
        session.add(comm)
        await session.commit()
        return '发表成功'
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        await session.rollback()
        # raise e
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='发表评论失败' + str(e))


async def get_post_comm(session: AsyncSession, pid: int) -> List[CommentPostOut]:
    try:
        # 查询所有顶级评论
        result = await session.execute(
            select(Comment).where(and_(Comment.post_id == pid, Comment.parent_id == 0, Comment.state == 1)))
        top_comments = result.scalars().all()

        # 递归查询子评论
        async def get_child_comments(comment):
            r = await session.execute(select(Comment).where(Comment.parent_id == comment.id, Comment.state == 1))
            child_comments = r.scalars().all()
            reply = None
            if child_comments:
                reply = [await get_child_comments(child) for child in child_comments]
            u = await session.execute(select(User).where(User.id == comment.uid))
            user: User | None = u.scalar_one_or_none()
            if user is None:
                user.username = '未知'
                user.avatar = 'default.jpg'
            return CommentPostOut(
                id_=comment.id,
                post_id=comment.post_id,
                parent_id=comment.parent_id,
                username=user.username,
                user_img=user.avatar,
                content=comment.content,
                reply=reply,
                created_at=comment.created_at
            )

        return [await get_child_comments(comment) for comment in top_comments]
    except Exception as e:
        await session.rollback()
        # raise e
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='查询评论失败' + str(e))


async def get_comm_to_user(session: AsyncSession, username: str) -> List[Optional[CommentUserOut]]:
    try:
        user = await get_user(session, username)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户不存在')
        pid_list = await session.execute(select(Post.id).where(Post.user_id == user.id_))
        pid_list = pid_list.scalars().all()
        comm_list = []
        if pid_list is None:
            return []
        for pid in pid_list:  # 每篇文章
            comm = await session.execute(select(Comment).where(Comment.post_id == pid))
            comm = comm.scalars().fetchall()
            for c in comm:  # 文章下的评论
                if comm is not None:
                    cuser = await session.execute(select(User).where(User.id == c.uid))
                    cuser = cuser.scalar_one()
                    comm_list.append(CommentUserOut(
                        id_=c.id,
                        post_id=c.post_id,
                        parent_id=c.parent_id,
                        username=cuser.username,
                        user_img=cuser.avatar,
                        content=c.content,
                        state=c.state,
                        created_at=c.created_at
                    ))
        # print(comm_list)
        return comm_list
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        await session.rollback()
        # raise e
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='查询用户失败' + str(e))


async def get_users_comm(session: AsyncSession, username: str) -> List[Optional[CommentUserOut]]:
    try:
        user = await get_user(session, username)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户不存在')
        comm = await session.execute(select(Comment).where(Comment.uid == user.id_))
        comm = comm.scalars().fetchall()
        comm_list = []
        for c in comm:
            comm_list.append(CommentUserOut(
                id_=c.id,
                post_id=c.post_id,
                parent_id=c.parent_id,
                username=user.username,
                user_img=user.avatar,
                content=c.content,
                state=c.state,
                created_at=c.created_at
            ))
        # print(comm_list)
        return comm_list
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        await session.rollback()
        # raise e
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='查询用户失败' + str(e))


async def review_comments(session: AsyncSession, username: str, cid: int, passed: bool):
    try:
        comm = await session.execute(select(Comment).where(Comment.id == cid))
        comm = comm.scalar_one_or_none()
        if comm is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='评论不存在')
        pid = comm.post_id
        post = await get_post_ById(session, pid)
        if username != post.author:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=f'这不是你的文章的评论,author:{post.author}')
        if passed:
            comm.state = 1
        if not passed:
            comm.state = 0
        await session.commit()

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        await session.rollback()
        # raise e
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='修改失败' + str(e))


async def del_comments(session: AsyncSession, username: str, cid: int):
    try:
        comm = await session.execute(select(Comment).where(Comment.id == cid))
        comm = comm.scalar_one_or_none()
        if comm is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='评论不存在')
        pid = comm.post_id
        post = await get_post_ById(session, pid)
        uid = (await get_user(session, username)).id_
        group_id = (await get_user(session, username)).group_id
        if username != post.author and uid != comm.uid and group_id != Ugroup.administrators.value:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'没有权限删除')

        # TODO:级联删除
        async def delete_comment(comid: int):
            sub_comments = (await session.execute(select(Comment).where(Comment.parent_id == comid))).scalars().all()
            for sub_comment in sub_comments:
                await delete_comment(sub_comment.id)  # 递归删除评论的子评论
            c = (await session.execute(select(Comment).where(Comment.id == comid))).scalar_one()  # 删除当前评论
            await session.delete(c)

        await delete_comment(comid=cid)
        await session.commit()
        return '删除成功'
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        await session.rollback()
        # raise e
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='删除失败' + str(e))
