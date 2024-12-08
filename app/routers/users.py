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
from app.services.users import UserServiceAdmin, email_validator

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


@router.put('/update_user/{user_id}', response_model=UserUpdate, tags=['users'])
async def update_user(user_id: int, user_update: UserUpdate, user: BaseUser = Depends(get_current_superuser),
                      session: AsyncSession = Depends(get_async_session)):
    service = UserServiceAdmin(session)
    res = await service.update_user(user_id, user_update)
    return res


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


@router.get('/get_user/{user_id}', tags=['users'])
async def get_user(user_id: int, user: BaseUser = Depends(get_current_superuser),
                   session: AsyncSession = Depends(get_async_session)):
    service = UserServiceAdmin(session)
    user = await service.get_user_data(user_id)
    return user


@router.get('/get_roles', tags=['users'])
async def get_roles(user: BaseUser = Depends(get_current_superuser),
                    session: AsyncSession = Depends(get_async_session)):
    service = UserServiceAdmin(session)
    roles = await service.get_roles()
    return roles


@router.post('/edit_user_role/{user_id}/{role_id}', tags=['users'])
async def edit_role(user_id: int, role_id: int, user: BaseUser = Depends(get_current_superuser),
                    session: AsyncSession = Depends(get_async_session)):
    service = UserServiceAdmin(session)
    result = await service.edit_user_role(user_id, role_id)
    return result


@router.delete('/delete_user/{user_id}', tags=['users'])
async def delete_user(user_id: int, user: BaseUser = Depends(get_current_superuser),
                      session: AsyncSession = Depends(get_async_session)):
    service = UserServiceAdmin(session)
    res = await service.delete_user(user_id)
    return res


@router.get('/is_admin', tags=['auth'])
async def check_is_admin(session: AsyncSession = Depends(get_async_session),
                         user: BaseUser = Depends(get_current_user)):
    service = UserServiceAdmin(session)

    return user.is_superuser


@router.get('/is_teacher')
async def check_is_teacher(session: AsyncSession = Depends(get_async_session),
                           user: BaseUser = Depends(get_current_user)):
    return user.role_id == 3


@router.get('/get_teachers')
async def get_teachers(session: AsyncSession = Depends(get_async_session)):
    service = UserServiceAdmin(session)
    teachers = await service.get_teachers()
    return teachers


@router.get('/validate_email')
async def validate_email(email: str):
    result = await email_validator(email)
    return result
