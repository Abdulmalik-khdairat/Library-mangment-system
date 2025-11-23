from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session

from application.DTOS.borrow_dto import BorrowRequest, to_borrow_entity, to_borrow_response
from application.auth.jwt_service import jwt_decode
from infrastructure.repositories.book_repository import book_repo
from infrastructure.repositories.borrow_repo import borrow_repo
from infrastructure.repositories.user_repository import user_repo


def borrow_book(book_id :int,borrow_req :BorrowRequest,db:Session ,user_id :int):


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


def return_book(borrow_id: int, db: Session, user_id :int):

    borrow_entity = borrow_repo['get_by_id'](db, borrow_id)
    if not borrow_entity:
        raise HTTPException(404, "Borrow record not found")
    if str(borrow_entity.user_id) != str(user_id):
        raise HTTPException(403, "You are not authorized to return this book")
    if borrow_entity.status != "BORROWED":
        raise HTTPException(400, "This book is not currently borrowed")

    current_time = datetime.now()
    due_date = borrow_entity.duo_date

    if current_time > due_date:
        borrow_entity.status = "OVERDUE"
    else:
        borrow_entity.status = "RETURNED"

    borrow_entity.returned_date = current_time
    borrow_entity.updated_at = current_time
    borrow_repo['update'](db, borrow_id, borrow_entity)

    available_book = book_repo['get_by_id'](db, borrow_entity.book_id)
    available_book.available_quantity += 1

    book_repo['update'](db, borrow_entity.book_id, available_book)
    return to_borrow_response(borrow_entity)


def get_borrow(db:Session ):

    borrow_entity = borrow_repo['get_all'](db)
    if not borrow_entity:
        raise HTTPException(404, "Borrow not found")
    return [to_borrow_response(borrow) for borrow in borrow_entity]

def get_borrow_by_user(user_id :int,db:Session ):

    borrow_entity = borrow_repo['get_by_user_id'](db, user_id)
    if not borrow_entity:
        raise HTTPException(404, "Borrow not found")
    return [to_borrow_response(borrow) for borrow in borrow_entity]



def get_overdue(db:Session):

    borrow_entity = borrow_repo['get_overdue'](db)
    if not borrow_entity:
        raise HTTPException(404, "Borrow not found")

    return [to_borrow_response(borrow) for borrow in borrow_entity]