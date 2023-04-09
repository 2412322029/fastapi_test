from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from sql import crud
from sql.database import get_session
from .token import get_current_user
from .verifyModel import TokenData, CommentIn, CommentInput, CommentPostOut, CommentUserOut

commentapp = APIRouter()


@commentapp.post("/new_comment", summary='发表评论', description='返回递归评论列表')
async def newComment(cin: CommentInput, session: AsyncSession = Depends(get_session),
                     current_user: TokenData = Depends(get_current_user)):
    return await crud.newComment(session, CommentIn(post_id=cin.post_id,
                                                    parent_id=cin.parent_id,
                                                    username=current_user.username,
                                                    content=cin.content
                                                    ))


@commentapp.get("/post_comm", summary='获取一篇文章评论', response_model=list[Optional[CommentPostOut]])
async def postComm(pid: int = Query(), session: AsyncSession = Depends(get_session)):
    return await crud.get_post_comm(session, pid)


@commentapp.get("/get_comm_to_user", summary='获取用户所有文章的评论', response_model=List[Optional[CommentUserOut]])
async def commToUser(username: str = Query(), session: AsyncSession = Depends(get_session)):
    return await crud.get_comm_to_user(session, username=username)


@commentapp.delete("/del_comments", summary='用户删除评论')
async def delComments(cid: int, session: AsyncSession = Depends(get_session), current_user: TokenData = Depends(get_current_user)):
    return await crud.del_comments(session, current_user.username, cid)
