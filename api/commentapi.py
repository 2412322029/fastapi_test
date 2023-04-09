from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from sql import crud
from sql.database import get_session
from .token import get_current_user
from .verifyModel import TokenData, CommentIn, CommentInput, CommentPostOut

commentapp = APIRouter()


@commentapp.post("/new_comment", summary='发表评论', description='返回递归评论列表')
async def new_comment(cin: CommentInput, session: AsyncSession = Depends(get_session),
                      current_user: TokenData = Depends(get_current_user)):
    return await crud.newComment(session, CommentIn(post_id=cin.post_id,
                                                    parent_id=cin.parent_id,
                                                    username=current_user.username,
                                                    content=cin.content
                                                    ))


@commentapp.get("/post_comm", summary='获取文章评论', response_model=list[CommentPostOut])
async def post_comm(pid: str = Query(default=..., max_length=30), session: AsyncSession = Depends(get_session)):
    return await crud.get_post_comm(session, pid)
