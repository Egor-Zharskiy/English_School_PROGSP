from typing import Optional

from fastapi_users import schemas, models
from pydantic import BaseModel


class UserRead(schemas.BaseUser[int]):
    username: str
    role_id: int


class UserCreate(schemas.BaseUserCreate):
    username: str
    role_id: int


class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None

    def create_update_dict_superuser(self):
        return self.model_dump(exclude_unset=True, exclude={"id"})



class BaseUser(BaseModel):
    id: int
    username: str
    email: str
