from sqlalchemy import select


from app.db.ext import connection
from app.db.users.schemas import UsersOrm

from app.models import UserBase, UserLogin, UserView, PageOptions, Role
from app.core.config import settings

from app.security.password import get_password_hash, verify_password

import app.security


@connection 
async def init_users(session):
    admin = UsersOrm(username='admin', 
                     email=settings.FIRST_SUPERUSER, 
                     password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD), 
                     is_activated=True, 
                     role=Role.ADMIN
    )
    session.add(admin)
    await session.commit()

@connection
async def get_users(options: PageOptions, session):
    result = await session.execute(select(UsersOrm).offset(options.offset).limit(options.limit))
    users = result.scalars().all()
    return users


@connection
async def get_user_by_username(username: str, session):
    result = await session.execute(select(UsersOrm).where(UsersOrm.username == username))
    user = result.scalars().first()
    return user


@connection
async def add_user(user: UserLogin, session, is_activated: bool =False, role: Role = Role.USER):
    new_user = UsersOrm(username=user.username, email=user.email, password=user.password, is_activated=is_activated, role=role)
    session.add(new_user)
    await session.commit()

@connection 
async def del_user(username: str, session):
    user = await get_user_by_username(username)
    if user:
        session.delete(user)
        await session.commit()

@connection 
async def activate_user(username: str, session):
    user = await get_user_by_username(username)
    if user:
        user.is_activated = True 
        await session.commit()

@connection 
async def deactivate_user(username: str, session):
    user = await get_user_by_username(username)
    if user:
        user.is_activated = False
        await session.commit()

@connection 
async def set_user_password(username: str, password: str, session):
    user = await get_user_by_username(username)
    if user: 
        user.password = password 
        await session.commit()


async def authenticate(user: UserLogin):
    db_user = await get_user_by_username(user.username)
    if not db_user:
        return None 
    if not verify_password(user.password, db_user.password):
        return None
    return db_user

