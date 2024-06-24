from fastapi import APIRouter
from core import settings
from .users import users_router

api_v1_router = APIRouter(prefix=settings.api.v1.prefix)

api_v1_router.include_router(users_router, prefix=settings.api.v1.users)
