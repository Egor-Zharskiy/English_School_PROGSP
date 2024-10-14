import logging

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from starlette.responses import JSONResponse

from app.models.courses import Language
from models.courses import CourseFormat, AgeGroup
from schemas.courses import LanguageSchema, CourseFormatSchema, AgeGroupSchema


class BaseService:
    def __init__(self, session: AsyncSession, logger_name: str):
        self.logger = logging.getLogger(logger_name)
        self.session = session


class LanguageService:
    def __init__(self, session: AsyncSession):
        self.logger = logging.getLogger("LanguageService")
        self.session = session

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
            return HTTPException(status_code=status.HTTP_409_CONFLICT,
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
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Language not found."
            )


class CourseFormatService:
    def __init__(self, session: AsyncSession):
        self.logger = logging.getLogger("LanguageService")
        self.session = session

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
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
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
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="CourseFormat not found."
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
            return None


class AgeGroupService:
    def __init__(self, session: AsyncSession):
        self.logger = logging.getLogger("LanguageService")
        self.session = session

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
