from datetime import datetime

from sqlalchemy import Column, String, Integer, Enum, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from infrastructure.db.base import Base


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    isbn = Column(String, unique=True, index=True)
    publish_date = Column(DateTime, default=datetime.utcnow)
    category = Column(String, index=True)
    total_quantity = Column(Integer, default=0)
    available_quantity = Column(Integer, default=0)
    description= Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author_id = Column('author_id', Integer, ForeignKey("users.id"), nullable=False, index=True)

    author = relationship("User", back_populates="books")
    borrows = relationship("Borrow", back_populates="book")