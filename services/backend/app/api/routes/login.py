
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from datetime import timedelta

import jwt
from jwt.exceptions import InvalidTokenError

from app.security.access_token import create_access_token, decode_access_token
from app.core.config import settings
from app.db.users.utils import get_user_by_username, authenticate
from app.db.users.schemas import UsersOrm
from app.models import UserView, UserLogin, Token

from pydantic import ValidationError
from typing import Annotated

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

TokenDep = Annotated[str, Depends(reusable_oauth2)]

router = APIRouter(prefix="/login", tags=["login"])

async def get_current_user(token: TokenDep) -> UsersOrm:
    try:
        token_data = decode_access_token(token)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await get_user_by_username(token_data['sub'])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_activated:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


@router.post("/access-token")
async def login_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await authenticate(UserLogin(username=form_data.username, password=form_data.password))
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_activated:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token = create_access_token(user.username, expires_delta=access_token_expires)
    )


CurrentUser = Annotated[UsersOrm, Depends(get_current_user)]

@router.post("/test-token", response_model=UserView)
async def login_test_token(current_user: CurrentUser):
    return current_user
