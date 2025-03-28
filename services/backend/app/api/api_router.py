from fastapi import APIRouter

from app.api.routes import admin

api_router = APIRouter()
api_router.include_router(admin.router)
