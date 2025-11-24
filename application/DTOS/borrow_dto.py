from datetime import datetime, timezone

from pydantic import BaseModel, Field

from domain.entity.borrow_entity import BorrowEntity
from domain.entity.status_enum import StatusEnum


class BorrowRequest(BaseModel):
    duo_date: datetime


class BorrowResponse(BaseModel):
    id: int
    book_id: int
    user_id: int
    borrowed_date: datetime
    returned_date: datetime | None = None
    status: StatusEnum
    duo_date: datetime
    created_at: datetime
    updated_at: datetime


def to_borrow_entity(borrow: BorrowRequest, user_id: int, book_id: int) -> BorrowEntity:



    return BorrowEntity(
        id=None,
        book_id=book_id,
        user_id=user_id,
        borrowed_date=datetime.now(),
        duo_date=borrow.duo_date,
        returned_date=None,
        status="BORROWED",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


def to_borrow_response(borrow: BorrowEntity) -> BorrowResponse:
    return BorrowResponse(
        id=borrow.id,
        book_id=borrow.book_id,
        user_id=borrow.user_id,
        borrowed_date=borrow.borrowed_date,
        returned_date=borrow.returned_date,
        status=borrow.status,
        duo_date=borrow.duo_date,
        created_at=borrow.created_at,
        updated_at=borrow.updated_at
    )