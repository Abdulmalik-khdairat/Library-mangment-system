from dataclasses import dataclass
from datetime import datetime

@dataclass
class BookEntity:
    id: int | None
    title: str
    isbn: str
    publish_date: datetime
    category: str
    total_quantity: int
    available_quantity: int
    description: str
    created_at: datetime
    updated_at: datetime
    author_id: int