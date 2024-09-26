from fastapi import FastAPI

from app.routers.users import router as auth_router
from app.routers.courses import router as courses_router

app = FastAPI(
    title="English School"
)

app.include_router(auth_router)
app.include_router(courses_router)