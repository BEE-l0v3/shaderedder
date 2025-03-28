
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/login", tags=["login"])

@router.post("access-token")
def login_access_token():
    pass
