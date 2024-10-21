import logging

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from fastapi.responses import JSONResponse

from app.models.courses import Language, Course, CourseLevel
from models.courses import CourseFormat, AgeGroup, Level
from schemas.courses import LanguageSchema, CourseFormatSchema, AgeGroupSchema, LevelSchema, CreateCourseSchema, \
    EditCourseSchema


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
            levels = result.scalars().all()
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
            stmt = select(Course).where(Course.id == course_id)
            result = await self.session.execute(stmt)
            course = result.scalars().one()
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
            statement = select(Course)
            result = await self.session.execute(statement)
            courses = result.scalars().all()
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
