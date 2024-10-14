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
from app.models.courses import Language
from app.schemas.courses import LanguageSchema
from app.services.courses import LanguageService
from schemas.courses import CourseFormatSchema, AgeGroupSchema
from services.courses import CourseFormatService, AgeGroupService

router = APIRouter(prefix="/courses", tags=['courses'])


@router.post("/create_language")
async def create_language(language: LanguageSchema, user: BaseUser = Depends(get_current_superuser),
                          session: AsyncSession = Depends(get_async_session)):
    language_service = LanguageService(session)
    result = await language_service.create_language(language)
    return result


@router.get("/get_languages")
async def get_languages(user: BaseUser = Depends(get_current_user),
                        session: AsyncSession = Depends(get_async_session)):
    language_service = LanguageService(session)
    languages = await language_service.get_languages()
    return languages


@router.patch("/edit_language")
async def edit_language(language_id: int, language: LanguageSchema, user: BaseUser = Depends(get_current_superuser),
                        session: AsyncSession = Depends(get_async_session)):
    language_service = LanguageService(session)
    edited_language = await language_service.edit_language(language_id, language)
    return edited_language


@router.delete("/delete_language")
async def delete_language(language_id: int, user: BaseUser = Depends(get_current_superuser),
                          session: AsyncSession = Depends(get_async_session)):
    language_service = LanguageService(session)
    edited_language = await language_service.delete_language(language_id)
    return edited_language


@router.get("/get_course_formats")
async def get_course_formats(user: BaseUser = Depends(get_current_user),
                             session: AsyncSession = Depends(get_async_session)):
    format_service = CourseFormatService(session)
    result = await format_service.get_formats()
    return result


@router.post("/create_course_format")
async def create_course_format(course_format: CourseFormatSchema, user: BaseUser = Depends(get_current_superuser),
                               session: AsyncSession = Depends(get_async_session)):
    format_service = CourseFormatService(session)
    format = await format_service.create_format(course_format)
    return format


@router.patch("/edit_course_format")
async def edit_course_format(format_id: int, new_format: CourseFormatSchema,
                             user: BaseUser = Depends(get_current_superuser),
                             session: AsyncSession = Depends(get_async_session)):
    format_service = CourseFormatService(session)
    result = await format_service.edit_format(format_id, new_format)
    return result


@router.delete("/delete_course_format")
async def delete_course_format(format_id: int, user: BaseUser = Depends(get_current_superuser),
                               session: AsyncSession = Depends(get_async_session)):
    format_service = CourseFormatService(session)
    result = await format_service.delete_format(format_id)
    return result


@router.post("/create_age_group")
async def create_age_group(data: AgeGroupSchema, BaseUser=Depends(get_current_superuser),
                           session: AsyncSession = Depends(get_async_session)):
    age_group_service = AgeGroupService(session)
    result = await age_group_service.create_age_group(data)
    return result

