from dataclasses import dataclass
from datetime import datetime



@dataclass
class BorrowEntity:
    id: int | None

    book_id: int
    user_id: int
    borrowed_date: datetime
    duo_date: datetime
    returned_date: datetime | None
    created_at: datetime
    updated_at: datetime
    status: str = "BORROWED"

