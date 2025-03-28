
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/register", tags=["register"])

@router.post("/")
def register():
    pass 

@router.post("/activate")
def activate():
    pass 

@router.post("/deactivate")
def deactivate():
    pass
