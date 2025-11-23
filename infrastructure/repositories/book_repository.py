
from infrastructure.repositories.generic_repo import create_generic_repository
from domain.entity.book_entity import BookEntity
from infrastructure.models.book_model import Book 

book_repo = create_generic_repository(
     model_cls=Book,
     domain_cls=BookEntity
 )



