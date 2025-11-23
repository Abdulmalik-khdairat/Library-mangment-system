from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from domain.entity.role_enum import RoleEnum
from domain.entity.user_entity import UserEntity
from infrastructure.models.user_model import User  # We'll need to create this model
from infrastructure.repositories.generic_repo import create_generic_repository

user_repo = create_generic_repository(
    model_cls=User,
    domain_cls=UserEntity
)

#
# def repo_create_user(db: Session, user_entity: UserEntity):
#
#     user = User(
#         username=user_entity.username,
#         email=user_entity.email,
#         full_name=user_entity.full_name,
#         role=user_entity.role,
#         is_active=user_entity.is_active,
#         hashed_password=user_entity.hashed_password,
#         created_at=user_entity.created_at,
#         updated_at=user_entity.updated_at
#
#     )
#
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user
#
# def get_by_username(db: Session, username: str):
#
#     return db.query(User).filter(User.username == username).first()
#
# def repo_get_current_user(db: Session, user_id: int):
#     res= db.query(User).filter(User.id == user_id).first()
#     return UserEntity(
#         id=res.id,
#         username=res.username,
#         email=res.email,
#         full_name=res.full_name,
#         role=res.role,
#         is_active=res.is_active,
#         hashed_password=res.hashed_password,
#         created_at=res.created_at,
#         updated_at=res.updated_at
#     )
#
# def repo_get_all_users (db: Session):
#     res = db.query(User).all()
#     #return as user entity
#     return [UserEntity(
#         id=user.id,
#         username=user.username,
#         email=user.email,
#         full_name=user.full_name,
#         role=user.role,
#         is_active=user.is_active,
#         hashed_password=user.hashed_password
#         ,created_at=user.created_at,
#         updated_at=user.updated_at
#     ) for user in res]
#
# def repo_update_user(db: Session, user_id: int, user_entity: UserEntity):
#     try:
#         user = db.query(User).filter(User.id == user_id).first()
#         if not user:
#             raise HTTPException(404, "User not found")
#         if user_entity.username is not None:
#             user.username = user_entity.username
#         if user_entity.email is not None:
#             user.email = user_entity.email
#         if user_entity.full_name is not None:
#             user.full_name = user_entity.full_name
#         if user_entity.role is not None:
#             user.role = user_entity.role
#         if user_entity.is_active is not None:
#             user.is_active = user_entity.is_active
#         if user_entity.hashed_password is not None:
#             user.hashed_password = user_entity.hashed_password
#         user.updated_at = datetime.now()
#         db.add(user)
#         db.commit()
#         db.refresh(user)
#         return UserEntity(
#             id=user.id,
#             username=user.username,
#             email=user.email,
#             full_name=user.full_name,
#             role=user.role,
#             is_active=user.is_active,
#             hashed_password=user.hashed_password,
#             created_at=user.created_at,
#             updated_at=user.updated_at
#         )
#     except Exception as e:
#         #doing rollback
#         db.rollback()
#         raise HTTPException(500, str(e))
#
#
#
# def repo_delete_user(db:Session, user_id: int):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(404, "User not found")
#     db.delete(user)
#     db.commit()
#
# def repo_update_user_role (db: Session, user_id: int, role: RoleEnum):
#     user = db.query(User).filter(User.id == user_id).first()
#     if user is None:
#         raise HTTPException(404, "User not found")
#     user.role = role
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return UserEntity(
#         id=user.id,
#         username=user.username,
#         email=user.email,
#         full_name=user.full_name,
#         role=user.role,
#         is_active=user.is_active,
#         hashed_password=user.hashed_password,
#         created_at=user.created_at,
#         updated_at=user.updated_at
#     )
#
