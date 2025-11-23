from fastapi import HTTPException
from sqlalchemy.orm import Session

from application.DTOS.book_dto import to_book_entity, to_book_response, CreateBookDto, to_book_entity_update
from application.auth.jwt_service import jwt_decode
from infrastructure.repositories.book_repository import book_repo


def create_book_service(book: CreateBookDto, db: Session,token: str):
    payload = jwt_decode(token)
    if payload.get("role") != "AUTHOR":
        raise HTTPException(status_code=403, detail="Only authors can create books")

    author_id = payload.get("id")
    if not author_id:
        raise HTTPException(status_code=400, detail="Invalid user token")

    book_entity = to_book_entity(book, author_id=author_id)
    if book_entity is None:
        raise HTTPException(status_code=400, detail="Invalid book data")

    return book_repo['create'](db,book_entity)

def get_all_books_service(db: Session,page: int, limit: int):
    res= book_repo['get_all'](db,page, limit)
    return [to_book_response(book) for book in res]

def get_book_by_id_service(book_id: int, db: Session):
    book = book_repo['get_by_id'](db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

def search_books_service(query: str, db: Session):
    return book_repo['search'](db, query)


def delete_book_service(book_id: int, db: Session,token):

    payloud = jwt_decode(token)
    if payloud.get("role") != "ADMIN":
        raise HTTPException(status_code=403, detail="Only admins can delete books")

    deleted= book_repo['delete'](db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")

    return {"message": "Book deleted successfully"}


def update_book_service(book_id: int, book: CreateBookDto, db: Session,token):
    author_id = book_repo['get_by_id'](db, book_id).author_id

    payloud = jwt_decode(token)
    if payloud.get("role") != "ADMIN" or payloud.get("id") != author_id:
        raise HTTPException(status_code=403, detail="Only admins can update books")

    entity =to_book_entity_update(book)
    updated= book_repo['update'](db, book_id, entity)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book updated successfully"}


# class BookService:
#     def __init__(self, db: Session):
#         self.db = db
#
#     def create_book(self, book, token):
#         # Decode and validate token
#         payload = jwt_decode(token)
#         if payload.get("role") != "AUTHOR":
#             raise HTTPException(status_code=403, detail="Only authors can create books")
#
#         # Get author_id from token
#         author_id = payload.get("id")
#         if not author_id:
#             raise HTTPException(status_code=400, detail="Invalid user token")
#
#         # Create book entity with author_id from token
#         book_entity = to_book_entity(book, author_id=author_id)
#         if book_entity is None:
#             raise HTTPException(status_code=400, detail="Invalid book data")
#
#         # Save to database
#         res=  repo_create_book(self.db, book_entity)
#
#         return to_book_response(res)
#
#     def get_all_books(self, page, limit):
#         res = repo_get_all_books(self.db, page, limit)
#         return [to_book_response(book) for book in res]
#
#     def get_book_by_id(self, id):
#         res = repo_get_book_by_id(self.db, id)
#         return to_book_response(res)
#
#     def search_books(self, query):
#         res = repo_search_books(self.db, query)
#         return [to_book_response(book) for book in res]
#
#
#
