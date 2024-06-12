from fastapi import APIRouter

from api_v1 import router_v1
from education.items_views import items_router
from users.views import users_router
from core.config import settings

education_router = APIRouter()

education_router.include_router(items_router, tags=["items"])
education_router.include_router(users_router, tags=["users"])
education_router.include_router(router_v1, prefix=settings.api_v1_prefix)
