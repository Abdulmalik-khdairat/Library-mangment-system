from fastapi import HTTPException, Depends
from jose import JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from application.DTOS.userdto import UserCreate, to_user_entity, to_user_response, update_to_entity, UserUpdate
from application.auth.jwt_service import create_access_token, jwt_decode, create_refresh_token
from application.auth.password_service import PasswordService
from domain.entity.role_enum import RoleEnum
from infrastructure.repositories.user_repository import user_repo
from jose import JWTError


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


def ser_refresh_token(token: str, db: Session):
    try:
        payload = jwt_decode(token)
        user_id = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Create a new access token with the same payload
        access_token = create_access_token({"id": user_id, "role": payload.get("role", "USER")})

        # Return the same refresh token and new access token
        return {
            "access_token": access_token,
            "refresh_token": token,  # Return the same refresh token
            "token_type": "bearer"
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")


def get_current_user_by_token(token: str, db: Session):
    payload = jwt_decode(token)
    user_id = payload.get("id")
    if user_id is None:
        raise HTTPException(401, "Invalid token")

    user= user_repo['get_by_id'](db, user_id)
    return to_user_response(user)


def retrieve_all_users(token: str, db: Session, page: int = None, limit: int = None):
    payloud = jwt_decode(token)
    if payloud.get("role") not in ["ADMIN", "EMPLOYEE"]:
        raise HTTPException(403, "Admins and Employees only")

    users = user_repo['get_all'](db, page, limit)
    return [to_user_response(user) for user in users]


def ser_get_user_by_id(id: int, token: str, db: Session):
    payloud = jwt_decode(token)
    if payloud.get("role") not in ["ADMIN","EMPLOYEE"]  and payloud.get("id") != id:
        raise HTTPException(403, "Admins and Employees only ")

    user= user_repo['get_by_id'](db, id)
    if not user:
        raise HTTPException(404, "User not found")
    return to_user_response(user)

def ser_update_user (id: int, user: UserUpdate, token: str, db: Session):
    payloud = jwt_decode(token)
    if payloud.get("role") != "ADMIN" and payloud.get("id") != id:
        raise HTTPException(403, "Admins same user only   ")

    user_entity = update_to_entity(user)
    res=user_repo['update'](db, id, user_entity)
    return  to_user_response(res)



def ser_delete_user(id:int, token:str, db:Session):
    payloud = jwt_decode(token)
    if payloud.get("role") != "ADMIN":
        raise HTTPException(403, "Admins only")
    del_user = user_repo['delete'](db, id)
    if not del_user:
        return HTTPException(404, "User not found")

    return HTTPException(200, "User deleted successfully")


def ser_update_user_role(id:int ,role:RoleEnum ,token:str, db:Session):
    payload = jwt_decode(token)
    if payload.get("role") != "ADMIN":
        raise HTTPException(403, "Admins only ")

    if not user_repo['update_role'](db, id, role):
        return HTTPException(404, "User not found")

    return HTTPException(200, "User role updated successfully")



#
# class UserService:
#     def __init__(self, db: Session):
#         self.db = db
#
#     def create_user(self, user: UserCreate):
#         user_entity = to_user_entity(user)
#         return repo_create_user(self.db, user_entity)
#
#     def authenticate_user(self, username: str, password: str):
#         user = get_by_username(self.db, username)
#         if not user:
#             return None
#         if not PasswordService.verify_password(password, user.hashed_password):
#             return None
#         return user
#
#     def login(self, username: str, password: str):
#         user = self.authenticate_user(username, password)
#         if not user:
#             return None
#
#         payload = {
#             "sub": user.username,
#             "id": user.id,
#             "role": user.role.value
#         }
#
#         token = create_access_token(payload, 60)
#         return {"access_token": token, "token_type": "bearer"}
#
#     def get_current_user(self, token: str):
#         payload = jwt_decode(token)
#         user_id = payload.get("id")
#
#         if user_id is None:
#             raise HTTPException(401, "Invalid token")
#
#         res= repo_get_current_user(self.db, user_id)
#         return to_user_response(res)
#
#
#     def get_all_users(self, token: str):
#         payload = jwt_decode(token)
#
#         if payload.get("role") != "ADMIN":
#             raise HTTPException(403, "Admins only")
#
#         res= repo_get_all_users(self.db)
#         print(type(res[0]))
#         return [to_user_response(user) for user in res]
#
#     def get_user_by_id(self, id, token):
#         payload = jwt_decode(token)
#         if payload.get("role") != "ADMIN":
#             raise HTTPException(403, "you are unauthorized Admin only ")
#         res= repo_get_current_user(self.db, id)
#         return to_user_response(res)
#
#     def update_user(self, id, user, token):
#         payload = jwt_decode(token)
#         if payload.get("role") != "ADMIN":
#             raise HTTPException(403, "you are unauthorized Admin only ")
#         user_entity = update_to_entity(user)
#         res= repo_update_user(self.db, id, user_entity)
#         return to_user_response(res)
#
#     def delete_user(self, id, token):
#         payload = jwt_decode(token)
#         if payload.get("role") != "ADMIN":
#             raise HTTPException(403, "you are unauthorized Admin only ")
#         repo_delete_user(self.db, id)
#         return {"message": "User deleted successfully"}
#
#     def update_user_role(self, id, role, token):
#         payloud =jwt_decode(token)
#         if payloud.get("role") != "ADMIN":
#             raise HTTPException(403, "you are unauthorized Admin only " )
#         return repo_update_user_role(self.db, id, role)
