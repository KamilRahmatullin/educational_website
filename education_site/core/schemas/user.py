from pydantic import BaseModel, ConfigDict


class BaseUser(BaseModel):
    name: str


class UserRead(BaseUser):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserCreate(BaseUser):
    pass
