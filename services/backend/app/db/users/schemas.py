from sqlalchemy import Date, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base 
from typing import Optional
from app.models import Role
import datetime

"""
class UsersOrm(Base):
    __tablename__       = 'Users'
    id                  = Column(Integer, primary_key=True, index=True)
    username            = Column(String, index=True, unique=True, nullable=False)
    email               = Column(String, index=True, unique=True, nullable=False)
    password            = Column(String)
    jwt_issue_date      = Column(Date, nullable=False)
    is_activated        = Column(Boolean, nullable=False)
    is_password_expired = Column(Boolean, nullable=False)
"""

class UsersOrm(Base):
    __tablename__ = 'Users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    is_activated: Mapped[bool] = mapped_column(default=False)
    role: Mapped[Role] = mapped_column(default=Role.USER)
