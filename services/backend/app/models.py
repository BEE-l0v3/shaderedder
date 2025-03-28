from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import conint
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
    email: EmailStr

class UserLogin(UserBase):
    password: str


class UserView(UserBase):
    id: int
    is_activated: bool
    role: Role

class PageOptions(BaseModel):
    limit: PageSize = PageSize.SMALL
    offset: conint(ge=0) = 0

class JWTPayload(BaseModel):
    sub: str 
    exp: datetime
