from datetime import datetime
from typing import Optional, List, Union

from pydantic import BaseModel, Field, EmailStr

from application.auth.password_service import PasswordService
from domain.entity.role_enum import RoleEnum
from domain.entity.user_entity import UserEntity




class UserCreate(BaseModel):
    """User registration model"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=5)
    full_name: str
    role: RoleEnum = RoleEnum.USER

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]


#mapper fun
class UserUpdate(BaseModel):
    password: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[RoleEnum] = None
    is_active: Optional[bool] = None


def to_user_response(user: UserEntity) -> UserResponse:
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )
def to_user_entity(user: UserCreate) -> UserEntity:
    return UserEntity(
        id=None,  # Will be set by the database
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=PasswordService.hash_password(user.password),
        role=user.role,
        created_at=datetime.now() ,
        updated_at=datetime.now()
    )

def update_to_entity(user: UserUpdate) -> UserEntity:
    hashed_password = PasswordService.hash_password(user.password) if user.password else None
    return UserEntity(
        id=None,  # Will be set by the database
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        role=user.role,
        updated_at=datetime.now()
    )