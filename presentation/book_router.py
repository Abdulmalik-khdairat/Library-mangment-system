from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from application.DTOS.book_dto import CreateBookDto
from application.auth.jwt_middleware import auther , admin_or_employee
from application.services import book_service
from infrastructure.db.base import get_db

router = APIRouter(prefix="/books", tags=["Books"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/")
def create_book(
    book: CreateBookDto,
    db:Session = Depends(get_db),
    user=Depends(auther),
):
    return book_service.create_book_service(book,db,user["id"])

@router.get("/")
def get_all_books(
    db:Session = Depends(get_db),
    page: int = 1,
    limit: int = 10,
):
    return book_service.get_all_books_service(db,page,limit)

@router.get("/search")
def search_books(
    query: str,
    db:Session = Depends(get_db),
):
    return book_service.search_books_service(query,db)

@router.get("/{id}")
def get_book_by_id(
    id: int,
    db:Session = Depends(get_db),
):
    return book_service.get_book_by_id_service(id,db)

@router.delete("/{id}")
def delete_book(
    id: int,
    db:Session = Depends(get_db),
    user =Depends(admin_or_employee)
    ):
    return book_service.delete_book_service(id,db)


@router.put("/{id}")
def update_book(
    id: int,
    book: CreateBookDto,
    db:Session = Depends(get_db),
    user  = Depends(admin_or_employee)
):
    return book_service.update_book_service(id,book,db)

