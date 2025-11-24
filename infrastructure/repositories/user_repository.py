from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from domain.entity.role_enum import RoleEnum
from domain.entity.user_entity import UserEntity
from infrastructure.models.user_model import User
from infrastructure.repositories.generic_repo import create_generic_repository

user_repo = create_generic_repository(
    model_cls=User,
    domain_cls=UserEntity
)
