
from app.models import UserRegister, Token
from app.db.users.utils import add_user, activate_user, deactivate_user
from app.security.access_token import create_access_token, decode_access_token
from app.core.config import settings
from app.email.utils import send_email, generate_account_activation_email

from fastapi import APIRouter, Depends, status, HTTPException

from jwt import InvalidTokenError 

router = APIRouter(prefix="/register", tags=["register"])

@router.post("/new")
async def register_account(user: UserRegister):
    if settings.emails_enabled:
        add_user(user)
        activation_token_expires = timedelta(minutes=settings.EMAIL_ACTIVATION_TOKEN_EXPIRE_MINUTES)
        token = create_access_token(user.username, activation_token_expires)
        page = generate_account_activation_email(user.email, user.username, token)
        send_email(user.email, subject=user.username, html_content=page)
    else:
        add_user(user, is_activated=True)


@router.post("/activate")
def activate_account(token: Token):
    try:
        payload = decode_access_token(token.access_token)
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    username = payload['sub']
    activate_user(username)

