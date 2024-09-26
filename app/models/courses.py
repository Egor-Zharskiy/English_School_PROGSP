from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Language(Base):
    __tablename__ = "language"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)


class Level(Base):
    __tablename__ = "level"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)


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
    start_level_id = Column(Integer, ForeignKey("level.id"), nullable=False)
    end_level_id = Column(Integer, ForeignKey("level.id"), nullable=False)
    group_size = Column(Integer, nullable=False)
    intensity = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    language_id = Column(Integer, ForeignKey("language.id"), nullable=False)
    format_id = Column(Integer, ForeignKey("course_format.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    age_group_id = Column(Integer, ForeignKey("age_group.id"), nullable=False)

# metadata = MetaData()
#
# language = Table(
#     "language",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name", String, nullable=False, unique=True),
#     Column("permissions", JSON),
# )
#
# level = Table(
#     "level",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name", String, nullable=False, unique=True),
#     Column("description", String, nullable=True),
# )
#
# course_format = Table(
#     "course_format",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name", String, unique=True, nullable=False)
# )
#
# age_group = Table(
#     "age_group",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name", String, nullable=False, unique=True),
#     Column("min_age", Integer, nullable=False),
#     Column("max_age", Integer, nullable=False)
# )
#
# course = Table(
#     "course",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name", String, nullable=False, unique=True),
#     Column("description", nullable=False),
#     Column("start_level_id", Integer, ForeignKey("level.id"), nullable=False),
#     Column("end_level_id", Integer, ForeignKey("level.id"), nullable=False),
#     Column("group_size", Integer, nullable=False),
#     Column("intensity", String, nullable=False),
#     Column("price", Float, nullable=False),
#     Column("language_id", Integer, ForeignKey("language.id"), nullable=False),
#     Column("format_id", Integer, ForeignKey("format.id"), nullable=False),
#     Column("is_active", Boolean, default=True),
#     Column("age_group_id", Integer, ForeignKey("age_group.id"), nullable=False),
#
# )

# course_teacher = Table(
#     "course_teacher",
#     metadata,
#     Column("course_id", Integer, ForeignKey("course.id"), primary_key=True),
#     Column("teacher_id", Integer, ForeignKey("teacher.id"), primary_key=True),
# )

# course
#   - is_active
#   - teacher_id
#   - description
#   - language
#   - start and end date
#   - level
#   - students_kolichestvo
#   - интенсивность
#   -
