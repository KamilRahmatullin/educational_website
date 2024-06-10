from fastapi import APIRouter

from users import crud
from users.schemas import CreateUser

users_router = APIRouter(prefix="/user")


@users_router.get("/")
def get_user(user: CreateUser):
    return {"message": "success", "email": user.email}


@users_router.post("/")
def create_user(user: CreateUser):
    return crud.create_user(user_in=user)
