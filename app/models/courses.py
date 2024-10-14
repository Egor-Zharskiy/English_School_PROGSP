from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, JSON
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Language(Base):
    __tablename__ = "language"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    rus_name = Column(String, nullable=False, unique=True)


class CourseFormat(Base):
    __tablename__ = "course_format"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class AgeGroup(Base):
    __tablename__ = "age_group"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    min_age = Column(Integer, nullable=False)
    max_age = Column(Integer, nullable=False)


class Course(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    group_size = Column(Integer, nullable=False)
    intensity = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    language_id = Column(Integer, ForeignKey("language.id"), nullable=False)
    format_id = Column(Integer, ForeignKey("course_format.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    age_group_id = Column(Integer, ForeignKey("age_group.id"), nullable=False)

    levels = relationship("CourseLevel", back_populates="course")


class Level(Base):
    __tablename__ = "level"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    courses = relationship("CourseLevel", back_populates="level")


class CourseLevel(Base):
    __tablename__ = "course_level"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    level_id = Column(Integer, ForeignKey("level.id"), nullable=False)
    level_type = Column(String, nullable=False)

    course = relationship("Course", back_populates="levels")
    level = relationship("Level", back_populates="courses")
