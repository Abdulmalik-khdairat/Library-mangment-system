from domain.entity.borrow_entity import BorrowEntity
from infrastructure.models.borrow_model import Borrow
from infrastructure.repositories.generic_repo import create_generic_repository
borrow_repo = create_generic_repository(
     model_cls=Borrow,
     domain_cls=BorrowEntity
 )