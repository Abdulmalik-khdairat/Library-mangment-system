from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from application.DTOS.userdto import UserUpdate
from application.services.user_service import  retrieve_all_users, ser_get_user_by_id, \
    ser_update_user, ser_delete_user, ser_update_user_role
from domain.entity.role_enum import RoleEnum
from infrastructure.db.base import get_db


router = APIRouter(prefix="/users", tags=["Users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

#get all the users with or without pagination
@router.get("")
def get_all_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
    page: int = None,
    limit: int = None
):
    now = datetime.now()
    print(now)
    return retrieve_all_users(token, db, page, limit)


@router.get("/{id}")
def get_user_by_id(
    id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    return ser_get_user_by_id(id,token,db)


@router.put("/{id}")
def update_user(
    id: int,
    user: UserUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    return ser_update_user(id, user, token, db)

@router.delete("/{id}")
def delete_user(
    id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    return ser_delete_user(id, token, db)

@router.put("/{id}/role")
def update_user_role(
    id: int,
    role: RoleEnum,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    return ser_update_user_role(id, role, token, db)

#this router is only for admin
#
# def get_user_service(db: Session = Depends(get_db)):
#     return UserService(db)
#
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
#
# @router.get("/")
# def get_all_users(
#     token: str = Depends(oauth2_scheme),
#     service: UserService = Depends(get_user_service)
# ):
#     return service.get_all_users(token)
#
# @router.get("/{id}")
# def get_user_by_id(
#     id: int,
#     token: str = Depends(oauth2_scheme),
#     service: UserService = Depends(get_user_service)
# ):
#     return service.get_user_by_id(id, token)
#
# @router.put("/{id}")
# def update_user(
#     id: int,
#     user: UserUpdate,
#     token: str = Depends(oauth2_scheme),
#     service: UserService = Depends(get_user_service)
# ):
#     return service.update_user(id, user, token)
#
# @router.delete("/{id}")
# def delete_user(
#     id: int,
#     token: str = Depends(oauth2_scheme),
#     service: UserService = Depends(get_user_service)
# ):
#     return service.delete_user(id, token)
#
# @router.put("/{id}/role")
# def update_user_role(
#     id: int,
#     role: RoleEnum,
#     token: str = Depends(oauth2_scheme),
#     service: UserService = Depends(get_user_service)
# ):
#     return service.update_user_role(id, role, token)
