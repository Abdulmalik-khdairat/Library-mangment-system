from datetime import datetime, date
from pydantic import Field, BaseModel, field_validator

from domain.entity.book_entity import BookEntity


class CreateBookDto(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Title of the book")
    isbn: str = Field(..., min_length=10, max_length=13, description="ISBN of the book")
    publish_date: str = Field(..., description="Publication date in YYYY-MM-DD format")
    category: str = Field(..., min_length=1, description="Book category")
    total_quantity: int = Field(..., gt=0, description="Total number of copies available")
    description: str = Field(..., min_length=1, description="Book description")

    @field_validator('publish_date')
    def validate_date_format(cls, v):
        try:
            # Try to parse the date to validate the format
            date.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError("Invalid date format. Please use YYYY-MM-DD")


class BookResponseDto(BaseModel):
    title: str
    isbn: str
    publish_date: datetime
    category: str
    total_quantity: int
    available_quantity: int
    description: str
    created_at: datetime
    updated_at: datetime


def to_book_response(book: BookEntity) -> BookResponseDto:
    return BookResponseDto(
    title=book.title,
    isbn=book.isbn,
    publish_date=book.publish_date,
    category=book.category,
    total_quantity=book.total_quantity,
    available_quantity=book.available_quantity,
    description=book.description,
    created_at=book.created_at,
    updated_at=book.updated_at
    )

def to_book_entity(book: CreateBookDto, author_id: int) -> BookEntity:
    # Convert the date string to a datetime object
    publish_date = datetime.fromisoformat(book.publish_date)
    
    return BookEntity(
        id=None,
        title=book.title,
        isbn=book.isbn,
        publish_date=publish_date,
        category=book.category,
        total_quantity=book.total_quantity,
        available_quantity=book.total_quantity,  # Initially all copies are available
        description=book.description,
        author_id=author_id,  # Using the correct field name after fixing the typo
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
def to_book_entity_update(book: CreateBookDto) -> BookEntity:
    # Convert the date string to a datetime object
    publish_date = datetime.fromisoformat(book.publish_date) if book.publish_date else None

    # For updates, we'll use None for fields that should be preserved from the existing record
    # The repository layer will handle not updating these None values
    return BookEntity(
        id=None,
        title=book.title,
        isbn=book.isbn,
        publish_date=publish_date,
        category=book.category,
        total_quantity=book.total_quantity,
        available_quantity=book.total_quantity,  # Update available_quantity to match total_quantity
        description=book.description,
        author_id=None,  # Preserve existing author_id
        created_at=None,  # Preserve existing created_at
        updated_at=datetime.now()
    )