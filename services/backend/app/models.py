from pydantic import (
                BaseModel,
                EmailStr,
                conint,
                field_validator,
)
from typing import Literal
from datetime import datetime
import enum 

class PageSize(int, enum.Enum):
    """
    Max users to return in a single request
    """
    SMALL = 15
    MEDIUM = 30
    LARGE = 50
    XLARGE = 100

class Role(int, enum.Enum):
    ADMIN = 1 
    USER = 2


class UserBase(BaseModel):
    username: str

class UserLogin(UserBase):
    password: str

class UserRegister(UserLogin):
    email: EmailStr

class UserView(UserBase):
    id: int
    is_activated: bool
    role: Role
    email: EmailStr

class PageOptions(BaseModel):
    limit: PageSize = PageSize.SMALL
    offset: conint(ge=0) = 0

class Token(BaseModel):
    access_token: str 
    token_type: str = 'bearer'

class EmailData(BaseModel):
    html_content: str
    subject: str

class Message(BaseModel):
    success: bool
    comment: str = ""

class MessageRegister(Message):
    activated: bool

class EmailStatus(BaseModel):
    status_code: int
    status_text: str
