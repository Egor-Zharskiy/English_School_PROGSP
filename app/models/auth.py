from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, JSON
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

