
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from application.DTOS.borrow_dto import BorrowRequest
from application.auth.jwt_middleware import user_role, admin_or_employee
from application.services import borrow_service
from infrastructure.db.base import get_db

router = APIRouter(prefix="/borrow", tags=["Borrow"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")



@router.post("/{book_id}", status_code=status.HTTP_201_CREATED)
async def borrow_book(
    book_id: int,
    borrow_request: BorrowRequest,
    db: Session = Depends(get_db),
    user = Depends(user_role)
        ):
    return borrow_service.borrow_book(book_id, borrow_request, db,user["id"])



@router.get("/")
async def get_borrow(
    db: Session = Depends(get_db),
    user=Depends(admin_or_employee)
        ):
    return borrow_service.get_borrow(db)

@router.get("/user/{user_id}")
async def get_borrow_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    user=Depends(admin_or_employee)
        ):
    return borrow_service.get_borrow_by_user(user_id, db)

@router.get("/overdue")
async def get_overdue(
    db: Session = Depends(get_db),
    user=Depends(admin_or_employee)
        ):
    return borrow_service.get_overdue(db)


@router.put("/{borrow_id}/return")
async def return_book(
    borrow_id: int,
    db: Session = Depends(get_db),
    user=Depends(user_role)
):

    return borrow_service.return_book(borrow_id, db, user["id"])

