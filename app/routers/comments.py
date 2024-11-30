from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from dependencies import get_current_user, get_current_superuser
from routers.courses import router
from services.courses import SchoolCommentsService

router = APIRouter(prefix="/comments", tags=['comments'])


@router.post('/add_school_comment')
async def add_school_comment(comment: str, session: AsyncSession = Depends(get_async_session),
                             BaseUser=Depends(get_current_user)):
    service = SchoolCommentsService(session)
    res = await service.add_school_comment(BaseUser.id, comment)
    return res


@router.post('/verify_comment')
async def verify_comment(comment_id: int, session: AsyncSession = Depends(get_async_session),
                         BaseUser=Depends(get_current_superuser)):
    service = SchoolCommentsService(session)
    res = await service.verify_comment(comment_id)
    return res


@router.delete('/delete_comment')
async def delete_comment(comment_id: int, session: AsyncSession = Depends(get_async_session),
                         BaseUser=Depends(get_current_superuser)):
    service = SchoolCommentsService(session)
    res = await service.delete_comment(comment_id)
    return res


@router.get('/get_unverified_comments')
async def get_unverified_comments(session: AsyncSession = Depends(get_async_session),
                                   BaseUser=Depends(get_current_superuser)):
    service = SchoolCommentsService(session)
    comments = await service.get_unverified_comments()
    return comments


@router.get('/get_verified_comments')
async def get_comments(session: AsyncSession = Depends(get_async_session)):
    service = SchoolCommentsService(session)
    comments = await service.get_verified_comments()
    return comments
