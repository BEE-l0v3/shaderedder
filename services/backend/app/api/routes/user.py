from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/users", tags=["login"])

@router.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


