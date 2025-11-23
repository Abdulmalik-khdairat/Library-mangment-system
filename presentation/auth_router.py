from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request ,Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from application.auth.jwt_service import create_access_token, jwt_decode, create_refresh_token
from application.services import user_service
from infrastructure.db.base import get_db
from application.DTOS.userdto import UserCreate

router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


db_dep= Annotated[Session, Depends(get_db)]
token_dep = Annotated[str, Depends(oauth2_scheme)]
form_dep = Annotated[OAuth2PasswordRequestForm, Depends()]

@router.post("/register")
def register_user(
    user: UserCreate,
    db: db_dep

):
    return user_service.create_user(user,db)

@router.post("/login")
def login_user(
        db: db_dep,
        form_data: form_dep,
):
    result = user_service.login(form_data.username, form_data.password, db)
    if not result:
        raise HTTPException(400, "Invalid username or password")
    return result

@router.get("/me")
def get_current_user(
    token:token_dep,
    db: db_dep,
    req:Request
):
    user_id = req.state.user_id
    print(user_id)
    if not user_id:
        raise HTTPException(401, "Invalid token")

    return user_service.get_current_user(db, user_id)






@router.post("/refresh")
def refresh_token(
    db: db_dep ,
    refresh_token: str = Body(..., embed=True),

):
    try:
        payload = jwt_decode(refresh_token)
    except:
        raise HTTPException(401, "Invalid or expired refresh token")

    user_id = payload.get("id")
    if not user_id:
        raise HTTPException(401, "Refresh token missing user_id")


    return user_service.refresh_token(user_id, db)
