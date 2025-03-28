from sqlalchemy import select

from app.db.ext import connection
from app.db.users.schemas import UsersOrm

from app.models import UserBase, UserLogin, UserView, PageOptions

import app.security


@connection
async def get_users(options: PageOptions, session):
    result = await session.execute(select(UsersOrm))
    users = result.scalars().all()
    users = [UserView(id=u.id, username=u.username, email=u.email, is_activated=u.is_activated) for u in users]
    return users


@connection
async def get_user_by_username(username: str):
    result = await session.execute(select(UsersOrm).where(UsersOrm.username == username))
    user = result.scalars().first()
    return UserView(id=user.id, username=user.username, email=user.email, is_activated=user.is_activated, role=user.role)


@connection
async def add_user(user: UserLogin, session):
    new_user = UsersOrm(username=user.username, email=user.email, password=user.password)
    session.add(new_user)
    await session.commit()


"""
@connection 
async def get_current_user(token: TokenDep, session) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await session.get(UserOrm, token_data.sub)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not user.is_activated:
        raise HTTPException(status_code=status.HTTP_400, detail="User is not activated")
    user = User(username=user.username, email=user.email, password=user.password)
    return user
"""
