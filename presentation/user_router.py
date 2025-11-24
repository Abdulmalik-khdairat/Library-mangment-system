from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from application.DTOS.userdto import UserUpdate
from application.auth.jwt_middleware import  admin_or_employee, admin_or_employee_or_user
from application.services import user_service
from domain.entity.role_enum import RoleEnum
from infrastructure.db.base import get_db


router = APIRouter(prefix="/users", tags=["Users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.get("")
def get_all_user(

    user = Depends(admin_or_employee),
    db: Session = Depends(get_db),
    page: int = 0,
    limit: int = 10
):
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user_service.retrieve_all_users(db, page, limit)

@router.get("/{id}")
def get_user_by_id(
    id: int,
    user=Depends(admin_or_employee_or_user),
    db: Session = Depends(get_db),
):

    return user_service.get_user_by_id(id, db)


@router.put("/{id}")
def update_user(
    id: int,
    user: UserUpdate,
    validate_user =Depends(admin_or_employee_or_user),
    db: Session = Depends(get_db)
):
    return user_service.update_user(id, user, db)

@router.delete("/{id}")
def delete_user(
    id: int,
    user=Depends(admin_or_employee_or_user),
    db: Session = Depends(get_db)
):
    return user_service.delete_user(id, db)

@router.put("/{id}/role")
def update_user_role(
    id: int,
    role: RoleEnum,
    user=Depends(admin_or_employee),
    db: Session = Depends(get_db)
):
    return user_service.update_user_role(id, role, db)
