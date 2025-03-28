from datetime import datetime, timedelta, timezone 
from typing import Any 

from app.models import JWTPayload

import jwt 

from app.core.config import settings

ALGORITHM = "HS256"

def create_access_token(payload: JWTPayload) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(access_token: str) -> JWTPayload:
    payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    payload = JWTPayload(payload)
    return payload

