from fastapi import Depends, APIRouter, status
from fastapi_users import FastAPIUsers
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.schemas.users import BaseUser
from app.dependencies import get_current_user, get_current_superuser
from app.database import get_async_session
from app.models.courses import Language
from app.schemas.courses import LanguageSchema, CreateCourseSchema, EditCourseSchema
from app.services.courses import LanguageService
from schemas.courses import CourseFormatSchema, AgeGroupSchema, LevelSchema
from services.courses import CourseFormatService, AgeGroupService, LevelService, CourseService

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


@router.get('/get_language_by_id')
async def get_language(language_id: int, user: BaseUser = Depends(get_current_user),
                       session: AsyncSession = Depends(get_async_session)):
    language_service = LanguageService(session)
    result = await language_service.get_language_by_id(language_id)
    return result


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


@router.get('/get_course_formats_by_id')
async def get_course_formats_by_id(format_id: int, user: BaseUser = Depends(get_current_user),
                                   session: AsyncSession = Depends(get_async_session)):
    format_service = CourseFormatService(session)
    result = await format_service.get_format_by_id(format_id)
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


@router.get('/get_age_group_by_id')
async def get_age_group_by_id(group_id: int, BaseUser=Depends(get_current_user),
                              session: AsyncSession = Depends(get_async_session)):
    age_group_service = AgeGroupService(session)
    result = await age_group_service.get_group_by_id(group_id)
    return result


@router.get("/get_age_groups")
async def get_age_groups(BaseUser=Depends(get_current_user),
                         session: AsyncSession = Depends(get_async_session)):
    age_group_service = AgeGroupService(session)
    result = await age_group_service.get_age_groups()
    return result


@router.delete("/delete_age_group")
async def delete_age_group(group_id: int, BaseUser=Depends(get_current_superuser),
                           session: AsyncSession = Depends(get_async_session)):
    age_group_service = AgeGroupService(session)
    result = await age_group_service.delete_age_group(group_id)
    return result


@router.patch("/edit_age_group")
async def edit_age_group(group_id: int, group: AgeGroupSchema, BaseUser=Depends(get_current_superuser),
                         session: AsyncSession = Depends(get_async_session)):
    age_group_service = AgeGroupService(session)
    result = await age_group_service.edit_age_group(group_id, group)
    return result


@router.post("/create_level")
async def create_level(data: LevelSchema, BaseUser=Depends(get_current_superuser),
                       session: AsyncSession = Depends(get_async_session)):
    level_service = LevelService(session)
    result = await level_service.create_level(data)
    return result


@router.get('/get_levels')
async def get_levels(BaseUser=Depends(get_current_user),
                     session: AsyncSession = Depends(get_async_session)):
    level_service = LevelService(session)
    result = await level_service.get_levels()
    return result


@router.get('/get_level_by_id')
async def get_level_by_id(level_id: int, BaseUser=Depends(get_current_user),
                          session: AsyncSession = Depends(get_async_session)):
    level_service = LevelService(session)
    result = await level_service.get_level_by_id(level_id)
    return result


@router.delete('/delete_level')
async def delete_level(level_id: int, BaseUser=Depends(get_current_superuser),
                       session: AsyncSession = Depends(get_async_session)):
    level_service = LevelService(session)
    result = await level_service.delete_level(level_id)
    return result


@router.patch('/edit_level')
async def edit_level(level_id: int, data: LevelSchema, BaseUser=Depends(get_current_superuser),
                     session: AsyncSession = Depends(get_async_session)):
    level_service = LevelService(session)
    result = await level_service.edit_level(level_id, data)
    return result


@router.post('/create_course')
async def create_course(data: CreateCourseSchema, BaseUser=Depends(get_current_superuser),
                        session: AsyncSession = Depends(get_async_session)):
    course_service = CourseService(session)
    result = await course_service.create_course(data)
    return result


@router.get('/get_course_by_id')
async def get_course_by_id(course_id: int, BaseUser=Depends(get_current_user),
                           session: AsyncSession = Depends(get_async_session)):
    course_service = CourseService(session)
    result = await course_service.get_course_by_id(course_id)
    return result


@router.get('/get_courses')
async def get_courses(BaseUser=Depends(get_current_user),
                      session: AsyncSession = Depends(get_async_session)):
    course_service = CourseService(session)
    result = await course_service.get_courses()
    return result


@router.delete('/delete_course')
async def delete_course(course_id: int, BaseUser=Depends(get_current_superuser),
                        session: AsyncSession = Depends(get_async_session)):
    course_service = CourseService(session)
    result = await course_service.delete_course(course_id)
    return result


@router.patch('/edit_course')
async def edit_course(course_id: int, data: EditCourseSchema, BaseUser=Depends(get_current_superuser),
                      session: AsyncSession = Depends(get_async_session)):
    course_service = CourseService(session)
    result = await course_service.edit_course(course_id, data)
    return result
