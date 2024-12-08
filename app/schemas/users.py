from datetime import datetime
from typing import Optional

from fastapi_users import schemas, models
from pydantic import BaseModel, ConfigDict


class UserRead(schemas.BaseUser[int]):
    username: str
    role_id: int


class UserCreate(schemas.BaseUserCreate):
    username: str
    first_name: str
    last_name: str
    phone_number: str
    role_id: int


class UserUpdate(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None

    def create_update_dict_superuser(self):
        return self.model_dump(exclude_unset=True, exclude={"id"})


class BaseUser(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    phone_number: str


class Role(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class GetUserAdminPage(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    model_config = ConfigDict(from_attributes=True)



class GetDetailedUserAdminPage(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    phone_number: str
    registered_at: datetime
    role: Role
    model_config = ConfigDict(from_attributes=True)
