from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserEntity:
    id: int| None
    username: str
    email: str
    full_name: str
    hashed_password: str
    # Optional fields with defaults
    role: str = 'user'  # Default role
    is_active: bool = True  # Default active status
    created_at: datetime | None = None  # Will be set by the database
    updated_at: datetime | None = None  # Will be set by the database

