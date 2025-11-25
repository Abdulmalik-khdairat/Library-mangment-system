from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Callable, Type, TypeVar, Generic, Any
from sqlalchemy import or_
from infrastructure.db.base import Base as SQLAlchemyBase

T = TypeVar('T', bound=SQLAlchemyBase)
D = TypeVar('D')

def create_generic_repository(
        model_cls: Type[T],
        domain_cls: Type[D]
) -> Any:
    def to_domain(model_obj):
        if model_obj is None:
            return None

        columns = {column.name for column in model_cls.__table__.columns}

        domain_fields = set(domain_cls.__annotations__.keys())

        data = {}
        for key, value in model_obj.__dict__.items():
            if key.startswith('_') or key not in domain_fields:
                continue

            if hasattr(value, 'value'):
                value = value.value

            data[key] = value

        return domain_cls(**data)

    def create(db:Session,domain):
        model = model_cls(**domain.__dict__)

        db.add(model)
        db.commit()
        db.refresh(model)
        return to_domain(model)

    def get_all(db, page=1, limit=10):

        try:
            page = max(1, int(page))
            limit = max(1, int(limit))
        except (ValueError, TypeError):
            page, limit = 1, 10
            
        query = db.query(model_cls)
        models = query.offset((page - 1) * limit).limit(limit).all()
        return [to_domain(model) for model in models]

    def get_by_id(db, id):
        model = db.query(model_cls).filter(model_cls.id == id).first()
        if not model:
            return None
        return to_domain(model)

    def search(db, query):
        models = db.query(model_cls).filter(
            or_
            (
                model_cls.title.contains(query),
                model_cls.isbn.contains(query),
                model_cls.category.contains(query),
                model_cls.description.contains(query)
            )
        )

        return [to_domain(model) for model in models]

    def delete(db, id):
        model = db.query(model_cls).filter(model_cls.id == id).first()
        if not model:
            return None
            

        if hasattr(model, 'borrows'):
            for borrow in model.borrows:
                db.delete(borrow)
                
        db.delete(model)
        db.commit()
        return to_domain(model)

    def update(db, id, domain):
        model = db.query(model_cls).filter(model_cls.id == id).first()
        if not model:
            return None
            
        columns = {column.name for column in model_cls.__table__.columns}
        
        for key, value in domain.__dict__.items():
            if key in columns and value is not None:

                if hasattr(value, 'value'):
                    setattr(model, key, value.value)
                else:
                    setattr(model, key, value)
        
        try:
            db.commit()
            db.refresh(model)
            return to_domain(model)
        except Exception as e:
            db.rollback()
            raise e

    def get_by_username(db, username):
        model = db.query(model_cls).filter(model_cls.username == username).first()
        if not model:
            return None
        return to_domain(model)


    def update_role(db, id, role):
        model = db.query(model_cls).filter(model_cls.id == id).first()
        if not model:
            return None
        model.role = role
        db.commit()
        db.refresh(model)
        if hasattr(model, 'to_dict'):
            return model.to_dict()
        return {'id': model.id, 'role': model.role}

    def get_by_email(db, email):
        model = db.query(model_cls).filter(model_cls.email == email).first()
        if not model:
            return None
        return to_domain(model)


    def get_by_user_id(db, user_id):
       model = db.query(model_cls).filter(model_cls.user_id == user_id).all()
       if not model:
           return None
       return [to_domain(model) for model in model]


    def get_overdue(db):
        model = db.query(model_cls).filter(model_cls.status == "OVERDUE").all()
        if not model:
            return None
        return [to_domain(model) for model in model]
    def get_returned(db):
        model= db.query(model_cls).filter(model_cls.status=="RETURNED").all()
        if not model:
            return None
        return [to_domain(model) for model in model]

    return {
        "create": create,
        "get_all":get_all,
        "get_by_id":get_by_id,
        "search":search,
        "delete":delete,
        "update":update,
        "get_by_username":get_by_username,
        "update_role":update_role,
        "get_by_email":get_by_email,
        "get_by_user_id":get_by_user_id,
        "get_overdue":get_overdue,
        "get_returned":get_returned
    }