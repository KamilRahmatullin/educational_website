from typing import Annotated

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.crud import get_all_users, create_user
from core import db_helper
from core.schemas import UserRead
from core.schemas.user import UserCreate

users_router = APIRouter(tags=['users'])


@users_router.get('/', response_model=list[UserRead])
async def get_users(session: Annotated[AsyncSession, Depends(db_helper.session_getter)]):
    users = await get_all_users(session=session)
    return users


@users_router.post('/', response_model=UserRead)
async def post_user(session: Annotated[AsyncSession, Depends(db_helper.session_getter)], user_create: UserCreate):
    user = await create_user(session=session, user_create=user_create)
    return user
