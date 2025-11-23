from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserEntity:
    id: int| None
    username: str
    email: str
    full_name: str
    hashed_password: str

    role: str = 'user'
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None

