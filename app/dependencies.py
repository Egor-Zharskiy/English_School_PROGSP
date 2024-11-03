from fastapi import Depends
from fastapi_users import FastAPIUsers
from app.models.courses import User
from app.utils.auth_manager import get_user_manager
from app.config.auth import auth_backend

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


def get_current_user(user: User = Depends(fastapi_users.current_user())):
    return user


def get_current_superuser(user: User = Depends(fastapi_users.current_user(active=True, superuser=True))):
    return user
