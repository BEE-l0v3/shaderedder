
from app.models import UserRegister, Token, Message
from app.db.users.utils import add_user, del_user, activate_user, deactivate_user
from app.security.access_token import create_access_token, decode_access_token
from app.core.config import settings
from app.email.utils import send_email, generate_account_activation_email

from fastapi import APIRouter, Depends, status, HTTPException

from datetime import timedelta

from jwt import InvalidTokenError 
from pydantic import ValidationError

router = APIRouter(prefix="/register", tags=["register"])

@router.post("/new")
async def register_account(user: UserRegister):
    if settings.emails_enabled:
        try:
            await add_user(user)
        except Exception as e:
            return Message(success=False, comment='user already exists');
        activation_token_expires = timedelta(minutes=settings.EMAIL_ACTIVATION_TOKEN_EXPIRE_MINUTES)
        token = create_access_token(user.username, activation_token_expires)
        page = generate_account_activation_email(user.email, user.username, token)
        try:
            response = send_email(email_to=user.email, subject=page.subject, html_content=page.html_content)
        except ValidationError as e:
            await del_user(user.username)
            raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="could not send validation email")
        return Message(success=True)
    else:
        try:
            await add_user(user, is_activated=True)
        except Exception as e:
            return Message(success=False, comment='user already exists')
        return Message(success=True)


@router.post("/confirm")
async def activate_account(token: Token):
    try:
        payload = decode_access_token(token.access_token)
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    username = payload['sub']
    try:
        await activate_user(username)
        return Message(success=True, comment="activated")
    except (ValidationError, InvalidTokenError, ValueError) as e:
        return Message(success=False, comment=str(e))

