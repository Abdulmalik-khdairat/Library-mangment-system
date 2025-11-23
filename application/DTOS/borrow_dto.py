from datetime import datetime, timezone

from pydantic import BaseModel, validator, Field

from domain.entity.borrow_entity import BorrowEntity
from domain.entity.status_enum import StatusEnum


class BorrowRequest(BaseModel):
    duo_date: datetime  # Changed from due_date to match the database model
    @validator('duo_date')
    def ensure_utc(cls, v):
        # If no timezone is provided, assume it's in UTC
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        # If timezone is provided, convert to UTC
        return v.astimezone(timezone.utc)


class BorrowResponse(BaseModel):
    id: int
    book_id: int
    user_id: int
    borrowed_date: datetime
    returned_date: datetime | None = None  # Made optional with default None
    status: StatusEnum
    duo_date: datetime  # Changed from due_date to match the database model
    created_at: datetime
    updated_at: datetime


def to_borrow_entity(borrow: BorrowRequest, user_id: int, book_id: int) -> BorrowEntity:
    # Get current time in UTC and convert to local timezone
    now = datetime.now(timezone.utc).astimezone()
    
    # The due_date is already in UTC from the validator
    due_date_utc = borrow.duo_date
    # Convert to local timezone for storage
    due_date_local = due_date_utc.astimezone()
    
    print(f"Received due_date (UTC): {due_date_utc}")
    print(f"Converted to local time: {due_date_local}")
    
    return BorrowEntity(
        id=None,
        book_id=book_id,
        user_id=user_id,
        borrowed_date=now,
        duo_date=due_date_local,  # Store in local timezone
        returned_date=None,
        status="BORROWED",
        created_at=now,
        updated_at=now
    )


def to_borrow_response(borrow: BorrowEntity) -> BorrowResponse:
    return BorrowResponse(
        id=borrow.id,
        book_id=borrow.book_id,
        user_id=borrow.user_id,
        borrowed_date=borrow.borrowed_date,
        returned_date=borrow.returned_date,
        status=borrow.status,
        duo_date=borrow.duo_date,  # Changed from due_date to duo_date
        created_at=borrow.created_at,
        updated_at=borrow.updated_at
    )