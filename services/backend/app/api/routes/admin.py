from app.models import UserRegister, PageOptions, PageSize, Role, UserView, Message
from app.db.users import get_users, add_user 
from app.api.routes.login import CurrentUser

from fastapi import APIRouter, Depends, status, HTTPException

from pydantic import ValidationError
from typing import List, Annotated


router = APIRouter(prefix="/admin", tags=["admin"])

async def get_current_user_admin(current_user: CurrentUser):
    if not current_user.role == Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only for admins")
    return current_user

def get_page_options(limit: PageSize = PageSize.SMALL, offset: int = 0):
    try:
        return PageOptions(limit=limit, offset=offset)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())

@router.get("/get-users", dependencies=[Depends(get_current_user_admin)], response_model=List[UserView])
async def router_get_users(options: PageOptions= Depends(get_page_options)):
    result = await get_users(options)
    return result

@router.post("/add-user", dependencies=[Depends(get_current_user_admin)])
async def router_add_user(user: UserRegister):
    try:
        await add_user(user, is_activated=True)
        return Message(success=True)
    except Exception as e:
        return Message(success=False)

