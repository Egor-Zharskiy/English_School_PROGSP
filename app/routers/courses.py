from typing import Optional

from fastapi import Depends, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from app.schemas.users import BaseUser
from app.dependencies import get_current_user, get_current_superuser
from app.database import get_async_session
from app.schemas.courses import LanguageSchema, CreateCourseSchema, EditCourseSchema
from app.services.courses import LanguageService, CourseGroupService, GradeService
from app.schemas.courses import CourseFormatSchema, AgeGroupSchema, LevelSchema, CreateCourseRequestSchema, \
    EditCourseRequest
from app.services.courses import CourseFormatService, AgeGroupService, LevelService, CourseService, CourseRequestService
from app.services.users import check_grade

router = APIRouter(prefix="/courses", tags=['courses'])


@router.post("/create_language")
async def create_language(language: LanguageSchema, user: BaseUser = Depends(get_current_superuser),
                          session: AsyncSession = Depends(get_async_session)):
    language_service = LanguageService(session)
    result = await language_service.create_language(language)
    return result


@router.get("/get_languages")
async def get_languages(session: AsyncSession = Depends(get_async_session)):
    language_service = LanguageService(session)
    languages = await language_service.get_languages()
    return languages


@router.get('/get_language_by_id/{language_id}')
async def get_language(language_id: int, user: BaseUser = Depends(get_current_user),
                       session: AsyncSession = Depends(get_async_session)):
    language_service = LanguageService(session)
    result = await language_service.get_language_by_id(language_id)
    return result


@router.patch("/edit_language/{language_id}")
async def edit_language(language_id: int, language: LanguageSchema, user: BaseUser = Depends(get_current_superuser),
                        session: AsyncSession = Depends(get_async_session)):
    language_service = LanguageService(session)
    edited_language = await language_service.edit_language(language_id, language)
    return edited_language


@router.delete("/delete_language/{language_id}")
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


@router.delete("/delete_age_group/{group_id}")
async def delete_age_group(group_id: int, BaseUser=Depends(get_current_superuser),
                           session: AsyncSession = Depends(get_async_session)):
    age_group_service = AgeGroupService(session)
    result = await age_group_service.delete_age_group(group_id)
    return result


@router.patch("/edit_age_group/{group_id}/")
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


@router.patch('/edit_level/{level_id}/')
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


@router.get('/get_course_by_id/{course_id}')
async def get_course_by_id(course_id: int, session: AsyncSession = Depends(get_async_session)):
    course_service = CourseService(session)
    result = await course_service.get_course_by_id(course_id)
    return result


@router.get('/get_courses')
async def get_courses(session: AsyncSession = Depends(get_async_session)):
    course_service = CourseService(session)
    result = await course_service.get_courses()
    return result


@router.get('/get_user_courses/{user_id}')
async def get_user_courses(user_id: Optional[int] = None, session: AsyncSession = Depends(get_async_session),
                           BaseUser=Depends(get_current_user)):
    service = CourseService(session)
    res = await service.get_user_courses(BaseUser.id if not user_id else user_id)
    return res


@router.delete('/delete_course')
async def delete_course(course_id: int, BaseUser=Depends(get_current_superuser),
                        session: AsyncSession = Depends(get_async_session)):
    course_service = CourseService(session)
    result = await course_service.delete_course(course_id)
    return result


@router.patch('/edit_course/{course_id}')
async def edit_course(course_id: int, data: EditCourseSchema, BaseUser=Depends(get_current_superuser),
                      session: AsyncSession = Depends(get_async_session)):
    course_service = CourseService(session)
    result = await course_service.edit_course(course_id, data)
    return result


@router.post('/create_course_request')
async def create_course_request(data: CreateCourseRequestSchema,
                                session: AsyncSession = Depends(get_async_session),
                                BaseUser=Depends(get_current_user)):
    request_service = CourseRequestService(session)
    user_id = BaseUser.id
    result = await request_service.create_course_request(user_id, data.course_id)
    return result


@router.delete('/delete_course_request/{course_id}')
async def delete_course_request(course_id: int, session: AsyncSession = Depends(get_async_session),
                                BaseUser=Depends(get_current_superuser)):
    request_service = CourseRequestService(session)
    result = await request_service.delete_course_request(course_id)
    return result


@router.patch('/edit_course_request/{course_request_id}')
async def edit_course_request(course_request_id: int, data: EditCourseRequest,
                              session: AsyncSession = Depends(get_async_session),
                              BaseUser=Depends(get_current_superuser)):
    request_service = CourseRequestService(session)
    result = await request_service.update_course_request(course_request_id, data)
    return result


@router.get('/get_course_requests')
async def get_course_requests(session: AsyncSession = Depends(get_async_session),
                              BaseUser=Depends(get_current_user)):
    request_service = CourseRequestService(session)
    result = await request_service.get_course_requests()
    return result


@router.get("/get_course_request/{request_id}")
async def get_course_request(request_id: int, session: AsyncSession = Depends(get_async_session),
                             BaseUser=Depends(get_current_user)):
    request_service = CourseRequestService(session)
    request = await request_service.get_course_request(request_id)
    return request


@router.get('/get_user_course_requests/{user_id}')
async def get_user_course_requests(user_id: Optional[int] = None, session: AsyncSession = Depends(get_async_session),
                                   BaseUser=Depends(get_current_user)):
    request_service = CourseRequestService(session)

    requests = await request_service.get_user_requests(
        BaseUser.id if not user_id else user_id)
    return requests


@router.post('/create_group/{course_id}/{teacher_id}/{group_name}')
async def create_group(course_id: int, teacher_id: int, group_name: str,
                       session: AsyncSession = Depends(get_async_session)):
    service = CourseGroupService(session)
    group = await service.create_group(course_id, group_name, teacher_id)
    return group


@router.post('/add_user_to_group/{group_id}/{user_id}')
async def add_user_to_group(group_id: int, user_id: int, session: AsyncSession = Depends(get_async_session),
                            BaseUser=Depends(get_current_superuser)):
    service = CourseGroupService(session)
    group = await service.add_user_to_group(group_id, user_id)
    return group


@router.get('/get_course_students')
async def get_course_students(course_id: int, session: AsyncSession = Depends(get_async_session),
                              BaseUser=Depends(get_current_superuser)):
    service = CourseGroupService(session)
    users = await service.get_group_students(course_id)
    return users


@router.get('/get_groups')
async def get_groups(session: AsyncSession = Depends(get_async_session),
                     BaseUser=Depends(get_current_superuser)):
    service = CourseGroupService(session)
    groups = await service.get_groups()
    return groups

# @router.get('/get_teacher_groups/{teacher_id}')
# async def


@router.get('/get_detailed_group/{group_id}')
async def get_detailed_group(group_id: int, session: AsyncSession = Depends(get_async_session),
                             BaseUser=Depends(get_current_superuser)):
    service = CourseGroupService(session)
    group = await service.get_detailed_group(group_id)
    return group


@router.get('/get_teacher_groups/{teacher_id}')
async def get_teacher_groups(teacher_id: int, session: AsyncSession = Depends(get_async_session),
                             BaseUser=Depends(get_current_user)):
    service = CourseGroupService(session)
    teacher_groups = await service.get_teacher_groups(teacher_id)
    return teacher_groups


@router.delete('/remove_user_from_group/{user_id}/{group_id}')
async def remove_user_from_group(user_id: int, group_id: int, session: AsyncSession = Depends(get_async_session),
                                 BaseUser=Depends(get_current_superuser)):
    service = CourseGroupService(session)
    result = await service.remove_user_from_group(user_id, group_id)
    return result


@router.post('/add_teacher_to_group/{group_id}/{teacher_id}')
async def add_teacher_to_group(group_id: int, teacher_id: int, session: AsyncSession = Depends(get_async_session),
                               BaseUser=Depends(get_current_superuser)):
    service = CourseGroupService(session)
    result = await service.assign_teacher_to_group(group_id, teacher_id)
    return result


@router.get('/get_student_marks')
async def get_student_marks(session: AsyncSession = Depends(get_async_session),
                            BaseUser=Depends(get_current_user)):
    service = GradeService(session)
    marks = await service.get_student_marks(BaseUser.id)
    return marks


@router.post('/add_mark/{user_id}/{group_id}')
async def add_mark(user_id: int, group_id: int, grade: int, comment: Optional[str] = None,
                   session: AsyncSession = Depends(get_async_session),
                   BaseUser=Depends(get_current_superuser)):
    if not check_grade(grade):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Отметка должна быть в диапазоне от 0 до 10."
        )
    service = GradeService(session)
    res = await service.add_grade(group_id, user_id, grade, comment)
    return res


@router.delete('/delete_mark/{grade_id}')
async def delete_mark(grade_id: int, session: AsyncSession = Depends(get_async_session),
                      BaseUser=Depends(get_current_superuser)):
    service = GradeService(session)
    res = await service.delete_grade(grade_id)
    return res


@router.patch('/edit_mark/{grade_id}')
async def edit_mark(grade_id: int, grade: int = None, comment: str = None,
                    session: AsyncSession = Depends(get_async_session),
                    BaseUser=Depends(get_current_superuser)):
    service = GradeService(session)
    print(comment, grade)
    res = await service.update_grade(grade_id, grade, comment)
    return res


@router.get('/get_group_marks/{group_id}')
async def get_group_marks(group_id: int, session: AsyncSession = Depends(get_async_session),
                          BaseUser=Depends(get_current_superuser)):
    service = GradeService(session)
    res = await service.get_group_marks(group_id)
    return res
