from typing import Optional, List

from pydantic import BaseModel


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
