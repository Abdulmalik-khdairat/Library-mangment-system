from dataclasses import dataclass
from datetime import datetime

from domain.entity.status_enum import StatusEnum


@dataclass
class BorrowEntity:
    id: int | None

    book_id: int
    user_id: int
    borrowed_date: datetime
    duo_date: datetime  # Changed from due_date to match the database model
    returned_date: datetime | None
    created_at: datetime
    updated_at: datetime
    status: str = "BORROWED"

