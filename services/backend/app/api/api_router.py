from fastapi import APIRouter

from app.api.routes import admin
from app.api.routes import login 
from app.api.routes import register

api_router = APIRouter()
api_router.include_router(admin.router)
api_router.include_router(login.router)
api_router.include_router(register.router)
