import logging
import re

from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound, IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from fastapi.responses import JSONResponse
from sqlalchemy.orm import joinedload

from app.models.courses import User, Role

from app.schemas.users import GetDetailedUserAdminPage, UserUpdate


class UserServiceAdmin:
    def __init__(self, session: AsyncSession):
        self.logger = logging.getLogger("UserServiceAdmin")
        self.session = session

    async def is_admin(self, user):
        return user.is_superuser

    async def get_user_data(self, user_id: int):
        try:
            stmt = select(User).where(User.id == user_id).options(
                joinedload(User.role)
            )
            result = await self.session.execute(stmt)
            user_query = result.scalars().one()
            user = GetDetailedUserAdminPage.model_validate(user_query).model_dump()
            return user
        except NoResultFound as e:
            self.logger.error(str(e))
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with given id not found")
        except Exception as e:
            self.logger.error(str(e))
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                 detail="An unexpected error occurred")

    async def update_user(self, user_id: int, user_update: UserUpdate):
        update_data = user_update.model_dump(exclude_unset=True)
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )

        try:
            result = await self.session.execute(stmt)

            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="Пользователь не найден")

            await self.session.commit()

        except SQLAlchemyError as e:
            self.logger.error(str(e))
            await self.session.rollback()
            raise HTTPException(status_code=500, detail=f"Ошибка базы данных: {str(e)}")

        return JSONResponse(status_code=status.HTTP_200_OK, content="Пользователь успешно обновлён")

    async def get_roles(self):
        stmt = select(Role)
        query = await self.session.execute(stmt)
        roles = query.scalars().all()
        return roles

    async def edit_user_role(self, user_id: int, role_id: int):
        try:
            role_check_stmt = select(Role).where(Role.id == role_id)
            role_check_result = await self.session.execute(role_check_stmt)
            role = role_check_result.scalar_one_or_none()

            if not role:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Указанная роль не найдена")

            stmt = (
                update(User)
                .where(User.id == user_id)
                .values(role_id=role_id)
                .execution_options(synchronize_session="fetch")
            )

            result = await self.session.execute(stmt)

            if result.rowcount == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

            await self.session.commit()

            return JSONResponse(status_code=status.HTTP_200_OK, content="Роль пользователя успешно обновлена")

        except SQLAlchemyError as e:
            self.logger.error(f"Ошибка базы данных: {str(e)}")
            await self.session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Ошибка базы данных: {str(e)}")
        except HTTPException as e:
            self.logger.error(f"Ошибка: {str(e.detail)}")
            raise e
        except Exception as e:
            self.logger.error(f"Неизвестная ошибка: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Произошла неожиданная ошибка")

    async def delete_user(self, user_id: int):
        stmt = delete(User).where(User.id == user_id)

        try:
            await self.session.execute(stmt)
            await self.session.commit()
            self.logger.info(f"user has been deleted: {user_id}")
            return JSONResponse(status_code=status.HTTP_200_OK, content="Deleted successfully")
        except Exception as e:
            self.logger.error(str(e))
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="An Error occured")

    async def get_teachers(self):
        stmt = select(User).where(User.role_id == 3)
        query = await self.session.execute(stmt)
        teachers = query.scalars().all()
        return teachers


async def email_validator(email: str) -> bool:
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if not re.match(email_regex, email):
        return False

    if len(email) > 320:
        return False
    if email.split("@")[1] in {"example.com", "test.com"}:
        return False

    return True


async def check_grade(grade):
    if isinstance(grade, int):
        return True if 0 <= grade <= 10 else False
    return False
