from app.db.users import get_users, add_user
from fastapi import APIRouter, Depends, HTTPException
from app.models import UserLogin, PageOptions
from typing import List

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/")
async def router_get_users(options: PageOptions= Depends()):
    #return {'users': None}
    result = await get_users(options)
    return result

@router.post("/add-user")
async def router_add_user(user: UserLogin):
    try:
        await add_user(user)
        return {'success': True}
    except Exception as e:
        return {'success': False}
