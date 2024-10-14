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
