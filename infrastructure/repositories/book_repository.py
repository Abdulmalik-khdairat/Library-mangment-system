# from fastapi import HTTPException
# from sqlalchemy.orm import Session
#
from infrastructure.repositories.generic_repo import create_generic_repository
from domain.entity.book_entity import BookEntity
from infrastructure.models.book_model import Book 
# from infrastructure.repositories.base_repository import
#
#
# def repo_create_book(db: Session, book_entity: BookEntity) -> BookEntity:
#
#
#
#

book_repo = create_generic_repository(
     model_cls=Book,
     domain_cls=BookEntity
 )





# def repo_create_book(db: Session, book_entity: BookEntity) -> BookEntity:
#     # Check if book with same ISBN already exists
#     if db.query(Book).filter(Book.isbn == book_entity.isbn).first() is not None:
#         raise HTTPException(status_code=400, detail="Book with this ISBN already exists")
#
#     try:
#         # Create SQLAlchemy model instance
#         db_book = entity_to_model(book_entity)
#
#         db.add(db_book)
#         db.commit()
#         db.refresh(db_book)
#
#         # Convert back to entity
#         return model_to_entity(db_book)
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=f"Failed to create book: {str(e)}")
#
#
# def repo_get_all_books(db: Session, page: int, limit: int):
#     books = db.query(Book).offset((page - 1) * limit).limit(limit).all()
#     return [model_to_entity(book) for book in books]
#
#
# def repo_get_book_by_id(db: Session, id: int):
#     book = db.query(Book).filter(Book.id == id).first()
#     if book is None:
#         raise HTTPException(status_code=404, detail="Book not found")
#     return model_to_entity(book)
#
#
# def repo_search_books(db: Session, query: str):
#     books = db.query(Book).filter(Book.title.contains(query)).all()
#     return [model_to_entity(book) for book in books]
#
#
#
#
#
#
# def entity_to_model(entity):
#     return Book(
#         title=entity.title,
#         isbn=entity.isbn,
#         publish_date=entity.publish_date,
#         category=entity.category,
#         total_quantity=entity.total_quantity,
#         available_quantity=entity.available_quantity,
#         description=entity.description,
#         author_id=entity.author_id,
#         created_at=entity.created_at,
#         updated_at=entity.updated_at
#     )
#
# def model_to_entity(model):
#     return BookEntity(
#         id=model.id,
#         title=model.title,
#         isbn=model.isbn,
#         publish_date=model.publish_date,
#         category=model.category,
#         total_quantity=model.total_quantity,
#         available_quantity=model.available_quantity,
#         description=model.description,
#         author_id=model.author_id,
#         created_at=model.created_at,
#         updated_at=model.updated_at
#     )
#
