from datetime import datetime
from typing import List

from sqlalchemy import Column, String, Integer, Enum, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from domain.entity.role_enum import RoleEnum
from infrastructure.db.base import Base





class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name= Column(String)
    role = Column(Enum(RoleEnum),default=RoleEnum.USER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationship with Book
    books = relationship("Book", back_populates="author")
    
    # Relationship with Borrow
    borrows = relationship("Borrow", back_populates="user")
