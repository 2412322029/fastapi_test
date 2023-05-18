from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from sql import crud
from sql.database import get_session
from .token import get_current_user
from .verifyModel import *

postapp = APIRouter()


@postapp.post("/new_post", summary='新建文章', response_model=PostOut)
async def newPost(post_in: PostIn, session: AsyncSession = Depends(get_session),
                  current_user: TokenData = Depends(get_current_user)):
    return await crud.new_post(session=session, a_post=PostInDB(username=current_user.username,
                                                                title=post_in.title,
                                                                content=post_in.content,
                                                                tag_names=post_in.tag_names))


@postapp.post("/new_tag", summary='新建tag')
async def newTag(atag: ANewTag, session: AsyncSession = Depends(get_session),
                 current_user: TokenData = Depends(get_current_user)):
    return await crud.new_tag(session=session, a_tag=atag)


@postapp.get("/get_all_posts_ByPage", summary='所有文章分页', response_model=PostOutPage)
async def getAllPosts(page: int = Query(default=1, gt=0), pagesize: int = Query(default=5, gt=0, lt=11),
                      session: AsyncSession = Depends(get_session)):
    return await crud.get_all_posts_ByPage(session=session, page=page, pagesize=pagesize)


@postapp.get("/get_users_posts", summary='用户文章分页', response_model=PostOutPage)
async def getUsersPosts(page: int = Query(default=1, gt=0), pagesize: int = Query(default=5, gt=0, lt=11),
                        username: str = Query(min_length=1, max_length=50),
                        session: AsyncSession = Depends(get_session)):
    return await crud.get_user_posts_ByPage(session=session, username=username, page=page,
                                            pagesize=pagesize)


@postapp.get("/get_post_ById", summary='获取文章详情', response_model=PostOut)
async def getPostById(pid: int = Query(gt=0), session: AsyncSession = Depends(get_session)):
    return await crud.get_post_ById(session, post_id=pid)


@postapp.get("/get_all_tags", summary='获取所有tag', response_model=list[TagInDB | None])
async def getAllTags(session: AsyncSession = Depends(get_session)):
    return await crud.get_all_tags(session)


@postapp.get("/get_user_all_tags", summary='获取用户所有tag', response_model=list[TagInDB | None])
async def getUserAllTags(username: str = Query(min_length=1, max_length=50),
                         session: AsyncSession = Depends(get_session)):
    return await crud.get_user_all_tags(session=session, username=username)


@postapp.get("/get_posts_ByTagPage",
             summary='获取该tag下的文章', response_model=PostOutPage)
async def getPostsByTagPage(tag_name: str = Query(min_length=1, max_length=50),
                            page: int = Query(default=1, gt=0), pagesize: int = Query(default=5, gt=0, lt=11),
                            session: AsyncSession = Depends(get_session)):
    return await crud.get_posts_ByTagPage(session=session, tag_name=tag_name, page=page, pagesize=pagesize)


@postapp.put("/updateTagCount", summary='更新tag计数')
async def updateTagCount(session: AsyncSession = Depends(get_session)):
    return await crud.updateTagCount(session)


@postapp.put("/update_post", summary='更新文章')
async def updatePost(pup: PostUpdate, session: AsyncSession = Depends(get_session),
                     current_user: TokenData = Depends(get_current_user)):
    return await crud.update_post_authorized(session, post_id=pup.pid,
                                             title=pup.title, content=pup.content,
                                             username=current_user.username)


@postapp.put("/add_tag_to_post", summary='给文章添加tag')
async def addTagTOPost(pid: int = Query(gt=0), tag_name: str = Query(max_length=50),
                       session: AsyncSession = Depends(get_session),
                       current_user: TokenData = Depends(get_current_user)):
    return await crud.add_tag_to_post_authorized(session, post_id=pid, tag_name=tag_name,
                                                 username=current_user.username)


@postapp.delete("/delete_post", summary='删除文章')
async def deletePost(pid: int = Query(gt=0), session: AsyncSession = Depends(get_session),
                     current_user: TokenData = Depends(get_current_user)):
    return await crud.delete_post(session, post_id=pid, username=current_user.username)


