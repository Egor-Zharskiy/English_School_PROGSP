from fastapi import Depends, APIRouter, status
from fastapi_users import FastAPIUsers
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.courses import User
from app.config.auth import auth_backend
from app.utils.auth_manager import get_user_manager
from app.schemas.users import UserRead, UserCreate, BaseUser, UserUpdate
from app.dependencies import get_current_user, get_current_superuser
from app.database import get_async_session

router = APIRouter(prefix="/auth")

fastapi_users = FastAPIUsers[BaseUser, int](
    get_user_manager,
    [auth_backend],
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    tags=["auth"],
)


@router.get('/verify_token', tags=['auth'])
async def verify_token(user: BaseUser = Depends(get_current_user)):
    return JSONResponse(status_code=status.HTTP_200_OK, content="Token is valid")


@router.get('/me', response_model=BaseUser, tags=['auth'])
async def get_me(user: BaseUser = Depends(get_current_user)):
    return user


@router.put('/me', response_model=UserUpdate, tags=['auth'])
async def update_me(user_update: UserUpdate, user: BaseUser = Depends(get_current_user),
                    user_manager=Depends(get_user_manager)):
    await user_manager.update(user_update, user)
    return user_update


@router.delete('/me', tags=['auth'])
async def delete_me(user: BaseUser = Depends(get_current_user), user_manager=Depends(get_user_manager)):
    await user_manager.delete(user)
    return JSONResponse(status_code=status.HTTP_200_OK, content="Account succesfully deleted")


@router.get('/users', tags=['auth'])
async def get_users(user: BaseUser = Depends(get_current_superuser),
                    session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users


@router.get('/get_roles', tags=['auth'])
async def get_roles(user: BaseUser = Depends(get_current_superuser)):
    ...


@router.post('/edit_user_role', tags=['auth'])
async def edit_role(user_id: int, role_id: int, user: BaseUser = Depends(get_current_superuser)):
    ...


@router.get('/is_admin', tags=['auth'])
async def check_is_admin(session: AsyncSession = Depends(get_async_session), user: BaseUser = Depends(get_current_user)):
    return user.is_superuser
