import datetime
import logging

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import NoResultFound, IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, insert, update
from fastapi.responses import JSONResponse
from sqlalchemy.orm import joinedload, class_mapper, selectinload
from starlette.status import HTTP_200_OK, HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE

from app.models.courses import Language, Course, CourseLevel, CourseGroup, User, GroupUser, Grade, SchoolComment
from app.models.courses import CourseFormat, AgeGroup, Level, CourseRequest
from app.schemas.courses import LanguageSchema, CourseFormatSchema, AgeGroupSchema, LevelSchema, CreateCourseSchema, \
    EditCourseSchema, CourseRequestResponse, EditCourseRequest, LevelAdminSchema, CourseRequestDetailedResponse, \
    CourseGroupSchema
from app.schemas.comments import VerifiedCommentsSchema, CommentsSchema


def model_to_dict(obj):
    return {column.name: getattr(obj, column.name) for column in class_mapper(obj.__class__).columns}


class BaseService:
    def __init__(self, session: AsyncSession, logger_name: str):
        self.logger = logging.getLogger(logger_name)
        self.session = session


class LanguageService:
    def __init__(self, session: AsyncSession):
        self.logger = logging.getLogger("LanguageService")
        self.session = session

    async def get_language_by_id(self, language_id: int):
        try:
            stmt = select(Language).where(Language.id == language_id)
            result = await self.session.execute(stmt)
            language = result.scalars().one()
            return language
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Language with id {language_id} not found."
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {str(e)}"
            )

    async def get_language_by_name(self, name: str):
        try:
            statement = select(Language).where(Language.name == name)
            result = await self.session.execute(statement)
            language = result.scalars().one()
            return language
        except NoResultFound as e:
            self.logger.error("NoResult " + str(e))
            return None
        except Exception as e:
            self.logger.error("Exception " + str(e))
            return None

    async def get_languages(self):
        try:
            statement = select(Language)
            result = await self.session.execute(statement)
            languages = result.scalars().all()
            return languages
        except NoResultFound as e:
            self.logger.error("Noresult " + str(e))
            return None
        except Exception as e:
            self.logger.error("Exception " + str(e))
            return None

    async def create_language(self, language_data: LanguageSchema):
        language = await self.get_language_by_name(language_data.name)
        if language:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Language with name {language.name} already exists")
        new_language = Language(name=language_data.name, rus_name=language_data.rus_name)
        self.session.add(new_language)
        await self.session.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(new_language))

    async def edit_language(self, language_id: int, language_data: LanguageSchema):
        try:
            statement = select(Language).where(Language.id == language_id)
            result = await self.session.execute(statement)
            existing_language = result.scalars().one()

        except NoResultFound as e:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                 detail="Language not found")
        existing_language.name, existing_language.rus_name = language_data.name, language_data.rus_name

        try:
            self.session.add(existing_language)
            await self.session.commit()
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content={"id": language_id, "name": existing_language.name,
                                         "rus_name": existing_language.rus_name})
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Language with this name already exists."
            )

    async def delete_language(self, language_id: int):
        try:
            stmt = delete(Language).where(Language.id == language_id)
            await self.session.execute(stmt)
            await self.session.commit()
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content="deleted successfully")

        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Language not found."
            )


class CourseFormatService:
    def __init__(self, session: AsyncSession):
        self.logger = logging.getLogger("LanguageService")
        self.session = session

    async def get_format_by_id(self, format_id: int):
        try:
            stmt = select(CourseFormat).where(CourseFormat.id == format_id)
            result = await self.session.execute(stmt)
            format = result.scalars().one()
            return format
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course format with id {format_id} not found."
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {str(e)}"
            )

    async def get_format_by_name(self, name: str):
        try:
            statement = select(CourseFormat).where(CourseFormat.name == name)
            result = await self.session.execute(statement)
            format = result.scalars().one()
            return format.name
        except NoResultFound as e:
            self.logger.error("NoResult " + str(e))
            return None
        except Exception as e:
            self.logger.error("Exception " + str(e))
            return None

    async def create_format(self, course_format: CourseFormatSchema):
        format = await self.get_format_by_name(course_format.name)
        if format:
            return HTTPException(status_code=status.HTTP_409_CONFLICT,
                                 detail=f"Course format {format} already exists")
        new_format = CourseFormat(name=course_format.name)
        try:
            self.session.add(new_format)
            await self.session.commit()
            return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(new_format))
        except Exception as e:
            self.logger.error(f"Error: {str(e)}")

    async def edit_format(self, format_id: int, new_format: CourseFormatSchema):
        try:
            statement = select(CourseFormat).where(CourseFormat.id == format_id)
            result = await self.session.execute(statement)
            existing_format = result.scalars().one()
        except NoResultFound as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Course format with given id not found")

        existing_format.name = new_format.name
        try:
            self.session.add(existing_format)
            await self.session.commit()
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content={"id": format_id, "name": existing_format.name})

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Course format with this name already exists."
            )

    async def delete_format(self, format_id: int):
        try:
            stmt = delete(CourseFormat).where(CourseFormat.id == format_id)
            await self.session.execute(stmt)
            await self.session.commit()
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content="deleted successfully")

        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course format not found."
            )

    async def get_formats(self):
        try:
            stmt = select(CourseFormat)
            result = await self.session.execute(stmt)
            formats = result.scalars().all()
            return formats
        except NoResultFound as e:
            self.logger.error("Noresult " + str(e))
            return None
        except Exception as e:
            self.logger.error("Exception " + str(e))
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course format's not found."
            )


class AgeGroupService:
    def __init__(self, session: AsyncSession):
        self.logger = logging.getLogger("LanguageService")
        self.session = session

    async def get_group_by_id(self, group_id: int):
        try:
            stmt = select(AgeGroup).where(AgeGroup.id == group_id)
            result = await self.session.execute(stmt)
            age_group = result.scalars().one()
            return age_group
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Age group with id {group_id} not found."
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {str(e)}"
            )

    async def create_age_group(self, data: AgeGroupSchema):
        statement = select(AgeGroup).where(AgeGroup.name == data.name)
        result = await self.session.execute(statement)
        existing_age_group = result.scalars().first()

        if existing_age_group:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Age group with this name already exists"
            )

        new_age_group = AgeGroup(
            name=data.name,
            min_age=data.min_age,
            max_age=data.max_age
        )

        self.session.add(new_age_group)
        await self.session.commit()
        await self.session.refresh(new_age_group)

        return new_age_group

    async def get_age_groups(self):
        try:
            stmt = select(AgeGroup)
            result = await self.session.execute(stmt)
            age_groups = result.scalars().all()
            return age_groups
        except NoResultFound as e:
            self.logger.error("Noresult " + str(e))
            return None
        except Exception as e:
            self.logger.error("Exception " + str(e))
            return None

    async def delete_age_group(self, group_id: int):
        try:
            stmt = delete(AgeGroup).where(AgeGroup.id == group_id)
            await self.session.execute(stmt)
            await self.session.commit()
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content="deleted successfully")

        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="AgeGroup not found."
            )

    async def edit_age_group(self, group_id: int, data: AgeGroupSchema):
        try:
            statement = select(AgeGroup).where(AgeGroup.id == group_id)
            result = await self.session.execute(statement)
            age_group = result.scalars().one()

            age_group.name = data.name
            age_group.min_age = data.min_age
            age_group.max_age = data.max_age

            self.session.add(age_group)
            await self.session.commit()

            return age_group

        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Age group not found"
            )

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Age group with this name already exists."
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )


class LevelService:
    def __init__(self, session: AsyncSession):
        self.logger = logging.getLogger("LevelService")
        self.session = session

    async def get_level_by_id(self, level_id: int):
        try:
            stmt = select(Level).where(Level.id == level_id)
            result = await self.session.execute(stmt)
            level = result.scalars().one()
            return level
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Level with id {level_id} not found."
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {str(e)}"
            )

    async def get_level_by_name(self, name: str):
        try:
            statement = select(Level).where(Level.name == name)
            result = await self.session.execute(statement)
            level = result.scalars().one()
            return level
        except NoResultFound as e:
            self.logger.error("NoResult for level " + str(e))
            return None
        except Exception as e:
            self.logger.error("Exception for level " + str(e))
            return None

    async def create_level(self, data: LevelSchema):
        level = await self.get_level_by_name(data.name)
        if level:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Level {level.name} {level.description} already exists")
        level = Level(name=data.name, description=data.description)
        try:
            self.session.add(level)
            await self.session.commit()
            return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(level))
        except Exception as e:
            self.logger.error(f"Error: {str(e)}")

    async def get_levels(self):
        try:
            stmt = select(Level)
            result = await self.session.execute(stmt)
            query = result.scalars().all()
            levels = [LevelAdminSchema.model_validate(item).model_dump() for item in query]
            return levels
        except NoResultFound as e:
            self.logger.error('NoResult ' + str(e))
            return None
        except Exception as e:
            self.logger.error("Exception " + str(e))
            return None

    async def delete_level(self, level_id: int):
        try:
            stmt = delete(Level).where(Level.id == level_id)
            await self.session.execute(stmt)
            await self.session.commit()
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content="deleted successfully")

        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Level not found."
            )

    async def edit_level(self, level_id: int, data: LevelSchema):
        try:
            statement = select(Level).where(Level.id == level_id)
            result = await self.session.execute(statement)
            level = result.scalars().one()

            level.name = data.name
            level.description = data.description

            self.session.add(level)
            await self.session.commit()

            return level

        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Level not found"
            )

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Level with this name already exists."
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )


class CourseService:
    def __init__(self, session: AsyncSession):
        self.logger = logging.getLogger("CourseService")
        self.session = session

    async def get_course_by_name(self, name: str):
        statement = select(Course).where(Course.name == name)
        result = await self.session.execute(statement)
        return result.scalars().first()

    async def create_course(self, course_data: CreateCourseSchema):
        existing_course = await self.get_course_by_name(course_data.name)
        if existing_course:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Course with name '{course_data.name}' already exists.")

        new_course = Course(
            name=course_data.name,
            description=course_data.description,
            group_size=course_data.group_size,
            intensity=course_data.intensity,
            price=course_data.price,
            language_id=course_data.language_id,
            format_id=course_data.format_id,
            is_active=course_data.is_active,
            age_group_id=course_data.age_group_id
        )

        self.session.add(new_course)

        try:
            await self.session.commit()
            await self.session.refresh(new_course)

            if course_data.levels:
                for level_id in course_data.levels:
                    new_course_level = CourseLevel(course_id=new_course.id, level_id=level_id, level_type="start_level")
                    self.session.add(new_course_level)

                await self.session.commit()

            return new_course

        except IntegrityError as e:
            self.logger.error("IntegrityError " + str(e))
            await self.session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Failed to create course due to a database constraint error.")

    async def get_course_by_id(self, course_id: int):
        try:
            stmt = (
                select(Course)
                .where(Course.id == course_id)
                .options(
                    joinedload(Course.format),
                    joinedload(Course.levels),
                    joinedload(Course.requests),
                    joinedload(Course.language)
                )
            )
            result = await self.session.execute(stmt)
            course = result.unique().scalars().one()
            return course
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with id {course_id} not found."
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {str(e)}"
            )

    async def get_courses(self):
        try:
            statement = select(Course).options(
                joinedload(Course.format),
                joinedload(Course.levels),
                joinedload(Course.requests),
                joinedload(Course.language)
            )

            result = await self.session.execute(statement)
            courses = result.unique().scalars().all()
            return courses
        except NoResultFound as e:
            self.logger.error("Noresult " + str(e))
            return None
        except Exception as e:
            self.logger.error("Exception " + str(e))
            return None

    async def delete_course(self, course_id: int):
        try:
            stmt = delete(Course).where(Course.id == course_id)
            await self.session.execute(stmt)
            await self.session.commit()
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content="deleted successfully")

        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found."
            )

    async def edit_course(self, course_id: int, course_data: EditCourseSchema):
        if course_data.name is not None:
            existing_course = await self.session.execute(
                select(Course).where(Course.name == course_data.name, Course.id != course_id)
            )
            existing_course = existing_course.scalars().first()

            if existing_course:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Course with this name already exists."
                )
        try:
            statement = select(Course).where(Course.id == course_id)
            result = await self.session.execute(statement)
            existing_course = result.scalars().one()
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found.")

        updatable_fields = [
            'name', 'description', 'group_size', 'intensity', 'price',
            'language_id', 'format_id', 'is_active', 'age_group_id'
        ]

        for field in updatable_fields:
            new_value = getattr(course_data, field)
            if new_value is not None:
                setattr(existing_course, field, new_value)

        if course_data.levels is not None:
            await self.session.execute(
                delete(CourseLevel).where(CourseLevel.course_id == course_id)
            )
            for level_id in course_data.levels:
                new_course_level = CourseLevel(course_id=course_id, level_id=level_id, level_type="start_level")
                self.session.add(new_course_level)

        try:
            self.session.add(existing_course)
            await self.session.commit()
            return {"message": "Course updated successfully"}
        except IntegrityError as e:
            await self.session.rollback()
            self.logger.error("IntegrityError " + str(e))
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Failed to update course due to a database constraint error.")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Unexpected error occurred" + str(e))

    async def get_user_courses(self, user_id: int):
        result = await self.session.execute(
            select(CourseGroup)
            .options(
                joinedload(CourseGroup.course),
                joinedload(CourseGroup.teacher)
            )
            .join(GroupUser, GroupUser.group_id == CourseGroup.id)
            .where(GroupUser.user_id == user_id)
        )
        course_groups = result.scalars().all()
        courses = [
            {
                "id": group.course.id,
                "name": group.course.name,
                "group_name": group.group_name,
            }
            for group in course_groups
        ]

        return courses


class CourseRequestService:
    def __init__(self, session: AsyncSession):
        self.logger = logging.getLogger("Course request service")
        self.session = session

    async def create_course_request(self, user_id: int, course_id: int):

        existing_course = await self.session.get(Course, course_id)
        if not existing_course:
            raise HTTPException(status_code=404, detail="Курс с данным ID не найден")

        existing_request = select(CourseRequest).where(CourseRequest.user_id == user_id,
                                                       CourseRequest.course_id == course_id)
        query = await self.session.execute(existing_request)
        existing_request = query.scalars().first()
        if existing_request:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Вы уже отправляли заявку на данный курс!!!")

        new_request = CourseRequest(
            user_id=user_id,
            course_id=course_id,
            status="pending",
            is_processed=False,
            is_archived=False
        )
        self.session.add(new_request)
        await self.session.commit()
        return JSONResponse(status_code=HTTP_200_OK,
                            content=CourseRequestResponse.model_validate(new_request).model_dump())

    async def delete_course_request(self, course_request_id: int):
        try:
            stmt = delete(CourseRequest).where(CourseRequest.id == course_request_id)
            await self.session.execute(stmt)
            await self.session.commit()
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content="deleted successfully")

        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course request not found."
            )

    async def update_course_request(self, request_id: int, data: EditCourseRequest):
        course_request = await self.session.get(CourseRequest, request_id)
        if not course_request:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="course request with given id not found")

        if data.status is not None:
            course_request.status = data.status
        if data.is_processed is not None:
            course_request.is_processed = data.is_processed
        if data.is_archived is not None:
            course_request.is_archived = data.is_archived

        self.session.add(course_request)
        await self.session.commit()
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=EditCourseRequest.model_validate(course_request).model_dump())

    async def get_course_requests(self):
        try:
            stmt = select(CourseRequest)
            result = await self.session.execute(stmt)
            requests = result.scalars().all()
            return requests

        except NoResultFound as e:
            self.logger.error("Noresult " + str(e))
            return None

        except Exception as e:
            self.logger.error("Exception " + str(e))
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course format's not found."
            )

    async def get_course_request(self, request_id: int):
        try:
            stmt = select(CourseRequest).where(CourseRequest.id == request_id).options(
                joinedload(CourseRequest.user),
                joinedload(CourseRequest.course).joinedload(Course.language)

            )
            query = await self.session.execute(stmt)
            course_request = query.scalars().one()
            filtered_request = CourseRequestDetailedResponse.model_validate(course_request).model_dump()
            return filtered_request
        except NoResultFound as e:
            self.logger.error(str(e))
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course request with given id not found")
        except Exception as e:
            self.logger.error(str(e))
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred")

    async def get_user_requests(self, user_id: int):
        stmt = (select(CourseRequest).where(CourseRequest.user_id == user_id)
        .options(
            joinedload(CourseRequest.course)
        ))
        result = await self.session.execute(stmt)
        requests = result.scalars().all()
        return requests


class CourseGroupService:
    def __init__(self, session):
        self.session = session
        self.logger = logging.getLogger("CourseGroupService")

    async def create_group(self, course_id: int, group_name: str, teacher_id: int):
        new_group = CourseGroup(course_id=course_id, group_name=group_name, teacher_id=teacher_id)
        self.session.add(new_group)
        await self.session.commit()
        return new_group

    async def add_user_to_group(self, group_id: int, user_id: int):
        group_exists = await self.session.execute(
            select(CourseGroup).where(CourseGroup.id == group_id)
        )
        user_exists = await self.session.execute(
            select(User).where(User.id == user_id)
        )

        group = group_exists.scalar_one_or_none()
        user = user_exists.scalar_one_or_none()

        if not group or not user:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content="Group or user not found"
            )

        user_in_group = await self.session.execute(
            select(GroupUser).where(
                (GroupUser.group_id == group_id) & (GroupUser.user_id == user_id)
            )
        )
        if user_in_group.scalar_one_or_none():
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content="User is already a member of this group"
            )

        try:
            stmt = insert(GroupUser).values(group_id=group_id, user_id=user_id)
            await self.session.execute(stmt)
            await self.session.commit()
            return JSONResponse(status_code=status.HTTP_200_OK, content="User added to group successfully")
        except SQLAlchemyError as e:
            await self.session.rollback()
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                content=f"Error while adding user to group: {str(e)}")

    async def assign_teacher_to_group(self, group_id: int, teacher_id: int):
        group_exists = await self.session.execute(
            select(CourseGroup).where(CourseGroup.id == group_id)
        )
        group = group_exists.scalar_one_or_none()

        teacher_exists = await self.session.execute(
            select(User).where(User.id == teacher_id)
        )
        teacher = teacher_exists.scalar_one_or_none()

        if not group or not teacher:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content="Group or teacher not found"
            )

        try:
            stmt = update(CourseGroup).where(CourseGroup.id == group_id).values(teacher_id=teacher_id)
            await self.session.execute(stmt)
            await self.session.commit()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content="Teacher assigned to group successfully"
            )
        except SQLAlchemyError as e:
            await self.session.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=f"Error while assigning teacher to group: {str(e)}"
            )

    async def get_group_students(self, course_id: int):
        try:
            stmt = (select(User)
                    .join(GroupUser, GroupUser.user_id == User.id)
                    .join(CourseGroup, CourseGroup.id == GroupUser.group_id)
                    .where(CourseGroup.course_id == course_id)
                    )
            result = await self.session.execute(stmt)
            users = result.scalars().all()
            return users
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=f"An error occured: {str(e)}")

    async def get_groups(self):
        try:
            stmt = select(CourseGroup).options(
                joinedload(CourseGroup.course),
                joinedload(CourseGroup.teacher),

            )

            query = await self.session.execute(stmt)
            groups = query.scalars().all()
            filtered_data = [CourseGroupSchema.model_validate(item).model_dump() for item in groups]
            return filtered_data
        except Exception as e:
            print(str(e))

    async def get_detailed_group(self, group_id: int):
        try:
            stmt = select(CourseGroup).where(CourseGroup.id == group_id).options(
                joinedload(CourseGroup.teacher),
                joinedload(CourseGroup.course),
                selectinload(CourseGroup.users)
            )
            query = await self.session.execute(stmt)
            group = query.scalars().one()
            return group
        except NoResultFound as e:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='group not found')
        except Exception as e:
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='an error occurred')

    async def remove_user_from_group(self, user_id: int, group_id: int):
        stmt = (
            delete(GroupUser)
            .where(GroupUser.group_id == group_id, GroupUser.user_id == user_id)
            .returning(GroupUser.id)
        )
        result = await self.session.execute(stmt)
        deleted_row = result.scalar_one_or_none()

        if deleted_row is None:
            raise NoResultFound(f"User {user_id} not found in group {group_id}.")

        await self.session.commit()
        return {"message": f"User {user_id} removed from group {group_id}."}

    async def get_teacher_groups(self, teacher_id: int):
        try:
            stmt = select(CourseGroup).where(CourseGroup.teacher_id == teacher_id)
            query = await self.session.execute(stmt)
            teacher_groups = query.scalars().all()
            return teacher_groups
        except NoResultFound as e:
            self.logger.error(f"error in get_teacher_groups: {str(e)}")
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group with given ID not found")
        # except Exception as e:
        #     return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred")


class GradeService:
    def __init__(self, session):
        self.session = session

    async def get_student_marks(self, user_id: int):
        grades = await self.session.execute(
            select(Grade).
            options(
                joinedload(Grade.group).joinedload(CourseGroup.course),
                joinedload(Grade.group).joinedload(CourseGroup.teacher)
            ).
            where(Grade.user_id == user_id).
            order_by(Grade.date_assigned.desc())
        )
        return grades.scalars().all()

    async def add_grade(self, group_id: int, user_id: int, grade: int, comments: str = None):
        group_exists = await self.session.execute(
            select(CourseGroup).where(CourseGroup.id == group_id)
        )
        group = group_exists.scalar_one_or_none()
        if not group:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content="Group not found"
            )

        user_exists = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        user = user_exists.scalar_one_or_none()
        if not user:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content="User not found"
            )

        user_in_group = await self.session.execute(
            select(GroupUser).where(
                (GroupUser.group_id == group_id) & (GroupUser.user_id == user_id)
            )
        )
        if not user_in_group.scalar_one_or_none():
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content="User is not a member of this group"
            )

        try:
            stmt = insert(Grade).values(
                group_id=group_id,
                user_id=user_id,
                grade=grade,
                comments=comments,
            )
            await self.session.execute(stmt)
            await self.session.commit()
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content="Grade added successfully"
            )
        except SQLAlchemyError as e:
            print(str(e))
            await self.session.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=f"Error while adding grade: {str(e)}"
            )

    async def delete_grade(self, grade_id: int):
        grade_exists = await self.session.execute(
            select(Grade).where(Grade.id == grade_id)
        )
        grade = grade_exists.scalar_one_or_none()
        if not grade:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content="Grade not found"
            )

        try:
            await self.session.delete(grade)
            await self.session.commit()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content="Grade deleted successfully"
            )
        except SQLAlchemyError as e:
            await self.session.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=f"Error while deleting grade: {str(e)}"
            )

    async def update_grade(self, grade_id: int, grade: float = None, comments: str = None):
        grade_exists = await self.session.execute(
            select(Grade).where(Grade.id == grade_id)
        )
        existing_grade = grade_exists.scalar_one_or_none()
        if not existing_grade:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content="Grade not found"
            )

        if grade is not None and (grade < 0 or grade > 10):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content="Grade must be between 0 and 10"
            )

        try:
            if grade is not None:
                existing_grade.grade = grade
            if comments is not None:
                existing_grade.comments = comments

            await self.session.commit()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content="Grade updated successfully"
            )
        except SQLAlchemyError as e:
            await self.session.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=f"Error while updating grade: {str(e)}"
            )

    async def get_group_marks(self, group_id: int):
        stmt = select(Grade).where(Grade.group_id == group_id).options(
            joinedload(Grade.user)
        )
        query = await self.session.execute(stmt)
        res = query.scalars().all()
        return res



class SchoolCommentsService:
    def __init__(self, session: AsyncSession):
        self.logger = logging.getLogger("SchoolCommentService")
        self.session = session

    async def add_school_comment(self, user_id: int, comment: str):
        if not comment.strip():
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content="Comment cannot be empty"
            )

        try:
            stmt = insert(SchoolComment).values(
                user_id=user_id,
                comment=comment,
            )
            await self.session.execute(stmt)
            await self.session.commit()
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content="Comment added successfully"
            )
        except SQLAlchemyError as e:
            await self.session.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=f"Error while adding comment: {str(e)}"
            )

    async def verify_comment(self, comment_id: int):
        try:
            stmt = update(SchoolComment).where(SchoolComment.id == comment_id).values(is_verified=True)
            await self.session.execute(stmt)
            await self.session.commit()
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content="Comment is verified"
            )
        except SQLAlchemyError as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=f"Error while verifying comment: {str(e)}"
            )

    async def delete_comment(self, comment_id: int):
        try:
            stmt = await self.session.execute(select(SchoolComment).where(SchoolComment.id == comment_id))
            comment = stmt.scalars().one()

            await self.session.delete(comment)
            await self.session.commit()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content="Comment deleted successfully")

        except NoResultFound:
            await self.session.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=f"Comment not found")
        except SQLAlchemyError as e:
            await self.session.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=f"Error while deleting comment: {str(e)}")

    async def get_verified_comments(self):
        stmt = select(SchoolComment).where(SchoolComment.is_verified == True).options(
            joinedload(SchoolComment.user)
        )

        query = await self.session.execute(stmt)
        comments = query.scalars().all()

        filtered_query = [VerifiedCommentsSchema.model_validate(comment).model_dump() for comment in comments]
        return filtered_query

    async def get_unverified_comments(self):
        stmt = select(SchoolComment).where(SchoolComment.is_verified == False)
        query = await self.session.execute(stmt)
        comments = query.scalars().all()
        return comments

    async def get_all_comments(self):
        stmt = select(SchoolComment).options(
            joinedload(SchoolComment.user)
        )
        query = await self.session.execute(stmt)
        comments = query.scalars().all()
        filtered_comments = [CommentsSchema.model_validate(comment).model_dump() for comment in comments]
        return filtered_comments
