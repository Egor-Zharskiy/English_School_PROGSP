from fastapi import Depends, APIRouter, status
from fastapi_users import FastAPIUsers
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.auth import User
from app.config.auth import auth_backend
from app.utils.auth_manager import get_user_manager
from app.schemas.users import UserRead, UserCreate, BaseUser, UserUpdate
from app.dependencies import get_current_user, get_current_superuser
from app.database import get_async_session
from app.schemas.courses import Language

router = APIRouter(prefix="/courses", tags=['courses'])

@router.post("/create_language")
async def create_language(language: Language, user: BaseUser = Depends(get_current_superuser)):
    print(language)

