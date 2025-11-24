from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from application.DTOS.userdto import UserCreate, to_user_entity, to_user_response, update_to_entity, UserUpdate
from application.auth.jwt_service import create_access_token, jwt_decode, create_refresh_token
from application.auth.password_service import PasswordService
from domain.entity.role_enum import RoleEnum
from infrastructure.repositories.user_repository import user_repo


def create_user(user: UserCreate, db: Session):

    if user_repo['get_by_username'](db, user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    existing_email = user_repo['get_by_email'](db, user.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered try to login or use another email")

    user_entity = to_user_entity(user)
    if user_entity.role not in [RoleEnum.USER, RoleEnum.AUTHOR]:
        raise HTTPException(status_code=400, detail="Role must be either USER or AUTHOR")

    return user_repo['create'](db, user_entity)

def login(username: str, password: str, db: Session):
    user= user_repo['get_by_username'](db, username)
    if not user :
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if not PasswordService.verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    role_value = user.role.value if hasattr(user.role, 'value') else user.role
    
    payload = {
        "sub": user.username,
        "id": user.id,
        "role": role_value
    }
    refresh_token = create_refresh_token(payload)

    token = create_access_token(payload)
    print(token)
    print(refresh_token)
    return {
        "access_token": token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


def refresh_token(token: str, db: Session):
    user = user_repo['get_by_id'](db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    print(user)
    payload = {
        "sub": user.username,
        "id": user.id,
        "role": user.role
    }
    token = create_access_token(payload)
    return {
        "access_token": token,
        "token_type": "bearer"
    }


def get_current_user(db: Session,user_id:int):

    user= user_repo['get_by_id'](db, user_id)
    return to_user_response(user)


def retrieve_all_users(db: Session, page: int = None, limit: int = None):


    users = user_repo['get_all'](db, page, limit)
    return [to_user_response(user) for user in users]


def get_user_by_id(id: int, db: Session):

    user= user_repo['get_by_id'](db, id)
    if not user:
        raise HTTPException(404, "User not found")
    return to_user_response(user)

def update_user (id: int, user: UserUpdate, db: Session):


    user_entity = update_to_entity(user)
    res=user_repo['update'](db, id, user_entity)
    return  to_user_response(res)



def delete_user(id:int,  db:Session):

    del_user = user_repo['delete'](db, id)

    if not del_user:
        return HTTPException(404, "User not found")

    return  {"status_code": 200, "detail": "User updated"}



def update_user_role(id:int ,role:RoleEnum , db:Session):


    if not user_repo['update_role'](db, id, role):
        return HTTPException(404, "User not found")

    return  {"status_code": 200, "detail": "User role updated"}


