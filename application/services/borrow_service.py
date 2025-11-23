from datetime import datetime , timezone
from zoneinfo import available_timezones

from fastapi import HTTPException
from sqlalchemy.orm import Session

from application.DTOS.borrow_dto import BorrowRequest, to_borrow_entity, to_borrow_response
from application.auth.jwt_service import jwt_decode
from infrastructure.repositories.book_repository import book_repo
from infrastructure.repositories.borrow_repo import borrow_repo
from infrastructure.repositories.user_repository import user_repo


def borrow_book_service(book_id :int,borrow_req :BorrowRequest,db:Session ,token :str):
    payloud = jwt_decode(token)
    if payloud.get("role") != "USER":
        raise HTTPException(403, "user only")
    user_id = payloud.get("id")

    borrow_entity = to_borrow_entity(borrow_req, user_id, book_id)
    available_book = book_repo['get_by_id'](db, book_id)

    if not available_book:
        raise HTTPException(404, "Book not found")
    if available_book.available_quantity <= 0:
        raise HTTPException(400, "Book is not available")
    available_book.available_quantity -= 1
    book_repo['update'](db, book_id, available_book)


    res= borrow_repo['create'](db, borrow_entity)
    return to_borrow_response(res)


def return_book_service(borrow_id: int, db: Session, token: str):
    payloud = jwt_decode(token)
    if payloud.get("role") != "USER":
        raise HTTPException(403, "User only")

    user_id = payloud.get("id")
    borrow_entity = borrow_repo['get_by_id'](db, borrow_id)
    if not borrow_entity:
        raise HTTPException(404, "Borrow record not found")
    if str(borrow_entity.user_id) != str(user_id):
        raise HTTPException(403, "You are not authorized to return this book")
    if borrow_entity.status != "BORROWED":
        raise HTTPException(400, "This book is not currently borrowed")

    # Get current time in UTC
    current_time = datetime.now().astimezone()  # This will use the system's local timezone

    # Make sure due_date is timezone-aware in the local timezone
    due_date = borrow_entity.duo_date
    if due_date.tzinfo is None:
        # If no timezone, assume it's in local time
        due_date = due_date.astimezone()
    else:
        # Convert to local timezone
        due_date = due_date.astimezone()


    # Compare in local time
    if current_time > due_date:
        borrow_entity.status = "OVERDUE"
    else:
        borrow_entity.status = "RETURNED"

    print(f"Status: {borrow_entity.status}")

    # Set returned date and update
    borrow_entity.returned_date = current_time
    borrow_entity.updated_at = current_time
    borrow_repo['update'](db, borrow_id, borrow_entity)

    available_book = book_repo['get_by_id'](db, borrow_entity.book_id)
    available_book.available_quantity += 1

    book_repo['update'](db, borrow_entity.book_id, available_book)
    return to_borrow_response(borrow_entity)


def get_borrow_service(db:Session ,token :str):
    payloud = jwt_decode(token)
    print(payloud.get("role"))
    if payloud.get("role")  not in ["ADMIN", "EMPLOYEE"]:
        raise HTTPException(403, "Admins and Employees only")

    borrow_entity = borrow_repo['get_all'](db)
    if not borrow_entity:
        raise HTTPException(404, "Borrow not found")
    return [to_borrow_response(borrow) for borrow in borrow_entity]

def get_borrow_by_user_service(user_id :int,db:Session ,token :str):
    payloud = jwt_decode(token)

    if payloud.get("role") not in ["ADMIN", "EMPLOYEE"] and str(payloud.get("id")) != str(user_id):
        raise HTTPException(403, "Only admins, employees, or the borrow owner can access this")

    borrow_entity = borrow_repo['get_by_user_id'](db, user_id)
    if not borrow_entity:
        raise HTTPException(404, "Borrow not found")
    return [to_borrow_response(borrow) for borrow in borrow_entity]



def get_overdue_service(db:Session,token:str):
    payloud = jwt_decode(token)
    if payloud.get("role") not in ["ADMIN", "EMPLOYEE"]:
        raise HTTPException(403, "Only admins and employees can access this")

    borrow_entity = borrow_repo['get_overdue'](db)
    if not borrow_entity:
        raise HTTPException(404, "Borrow not found")

    return [to_borrow_response(borrow) for borrow in borrow_entity]