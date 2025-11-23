from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from application.DTOS.borrow_dto import BorrowRequest
from application.services.borrow_service import borrow_book_service, return_book_service, get_borrow_service, \
    get_borrow_by_user_service, get_overdue_service
from infrastructure.db.base import get_db

router = APIRouter(prefix="/borrow", tags=["Borrow"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")



@router.post("/{book_id}", status_code=status.HTTP_201_CREATED)
async def borrow_book(
    book_id: int,
    borrow_request: BorrowRequest,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)

        ):
    return borrow_book_service(book_id, borrow_request, db, token)



@router.get("/")
async def get_borrow(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
        ):
    return get_borrow_service( db, token)

@router.get("/user/{user_id}")
async def get_borrow_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
        ):
    return get_borrow_by_user_service(user_id, db, token)

@router.get("/overdue")
async def get_overdue(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
        ):
    return get_overdue_service(db, token)


@router.put("/{borrow_id}/return")
async def return_book(
    borrow_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
        ):
    return return_book_service(borrow_id, db, token)

