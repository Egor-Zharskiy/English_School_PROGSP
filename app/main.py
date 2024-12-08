import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.users import router as auth_router
from app.routers.courses import router as courses_router
from app.routers.comments import router as comments_router

app = FastAPI(
    title="English School"
)

app.include_router(auth_router)
app.include_router(courses_router)

app.include_router(comments_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
