from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from sql import crud
from sql.database import get_session
from .token import get_current_user
from .verifyModel import UserOut, TokenData

postapp = APIRouter()


@postapp.get("/test")
async def userinfo(session: Session = Depends(get_session), current_user: TokenData = Depends(get_current_user)):
    return current_user
