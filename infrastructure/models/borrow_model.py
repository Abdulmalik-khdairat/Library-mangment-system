from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime,Enum
from sqlalchemy.orm import relationship

from domain.entity.status_enum import StatusEnum
from infrastructure.db.base import Base

class Borrow(Base):

    __tablename__= "borrow"

    id=Column(Integer,primary_key=True,index=True)
    book_id=Column(Integer,ForeignKey("books.id"),nullable=False,index=True)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False,index=True)
    borrowed_date=Column(DateTime,default=datetime.utcnow)
    duo_date =Column(DateTime )
    returned_date=Column(DateTime,default=None ,nullable=True)
    status=Column(Enum(StatusEnum),default=StatusEnum.BORROWED)
    created_at=Column(DateTime,default=datetime.utcnow)
    updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

    book=relationship("Book",back_populates="borrows")
    user=relationship("User",back_populates="borrows")