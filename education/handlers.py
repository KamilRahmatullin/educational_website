from fastapi import APIRouter

from education.items_views import items_router
from users.views import users_router

education_router = APIRouter()

education_router.include_router(items_router, tags=['items'])
education_router.include_router(users_router, tags=['users'])
