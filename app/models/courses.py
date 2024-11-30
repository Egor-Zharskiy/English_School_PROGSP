from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, JSON, TIMESTAMP, Text
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    permissions = Column(JSON)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String(15), unique=True)
    hashed_password = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.now)
    role_id = Column(Integer, ForeignKey("role.id"))
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    requests = relationship("CourseRequest", back_populates="user")
    groups = relationship("CourseGroup", secondary="group_user", back_populates="users")
    teacher_groups = relationship("CourseGroup", back_populates="teacher")
    school_comments = relationship("SchoolComment", back_populates="user", cascade="all, delete-orphan")


class CourseRequest(Base):
    __tablename__ = "course_request"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    is_processed = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)

    user = relationship("User", back_populates="requests")
    course = relationship("Course", back_populates="requests")


class CourseGroup(Base):
    __tablename__ = "course_group"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    group_name = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    course = relationship("Course", back_populates="groups")
    users = relationship("User", secondary="group_user", back_populates="groups")
    teacher = relationship("User", back_populates="teacher_groups")


class GroupUser(Base):
    __tablename__ = "group_user"

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("course_group.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    group = relationship("CourseGroup", overlaps="users,groups")
    user = relationship("User", overlaps="users,groups")


class Language(Base):
    __tablename__ = "language"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    rus_name = Column(String, nullable=False, unique=True)
    courses = relationship("Course", back_populates="language")


class CourseFormat(Base):
    __tablename__ = "course_format"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    courses = relationship("Course", back_populates="format")


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
    requests = relationship("CourseRequest", back_populates="course")
    groups = relationship("CourseGroup", back_populates="course")
    format = relationship("CourseFormat", back_populates="courses")
    language = relationship("Language", back_populates="courses")


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


class Grade(Base):
    __tablename__ = "grade"

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("course_group.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    grade = Column(Integer, nullable=False)
    comments = Column(String, nullable=True)
    date_assigned = Column(DateTime, default=datetime.utcnow, nullable=False)

    group = relationship("CourseGroup")
    user = relationship("User")


class SchoolComment(Base):
    __tablename__ = 'school_comments'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text, nullable=False)
    date_added = Column(DateTime, default=datetime.utcnow)
    is_verified = Column(Boolean, default=False)

    user = relationship("User", back_populates="school_comments")
