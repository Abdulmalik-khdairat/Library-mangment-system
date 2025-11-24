from fastapi import HTTPException
from sqlalchemy.orm import Session

from application.DTOS.book_dto import to_book_entity, to_book_response, CreateBookDto, to_book_entity_update
from infrastructure.repositories.book_repository import book_repo


def create_book_service(book: CreateBookDto, db: Session,author_id: int):


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


def delete_book_service(book_id: int, db: Session):


    deleted= book_repo['delete'](db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")

    return {"message": "Book deleted successfully"}


def update_book_service(book_id: int, book: CreateBookDto, db: Session):

    entity =to_book_entity_update(book)
    updated= book_repo['update'](db, book_id, entity)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book updated successfully"}


