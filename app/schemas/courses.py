from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class LanguageSchema(BaseModel):
    name: str
    rus_name: str


class CourseFormatSchema(BaseModel):
    name: str


class AgeGroupSchema(BaseModel):
    name: str
    min_age: int
    max_age: int


class LevelSchema(BaseModel):
    name: str
    description: str


class CreateCourseSchema(BaseModel):
    name: str
    description: str
    group_size: int
    intensity: str
    price: int
    language_id: int
    format_id: int
    is_active: Optional[bool] = None
    age_group_id: int
    levels: List[int]


class EditCourseSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    group_size: Optional[int] = None
    intensity: Optional[str] = None
    price: Optional[int] = None
    language_id: Optional[int] = None
    format_id: Optional[int] = None
    is_active: Optional[bool] = None
    age_group_id: Optional[int] = None
    levels: Optional[List[int]] = None


class CreateCourseRequestSchema(BaseModel):
    course_id: int


class CourseRequestResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    status: str
    is_processed: bool
    is_archived: bool

    model_config = ConfigDict(from_attributes=True)


class EditCourseRequest(BaseModel):
    status: Optional[str] = None
    is_processed: Optional[bool] = None
    is_archived: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)
