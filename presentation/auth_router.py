from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from application.auth.jwt_service import create_access_token, jwt_decode, create_refresh_token
from application.services.user_service import create_user, login, get_current_user_by_token, ser_refresh_token
from infrastructure.db.base import get_db
from application.DTOS.userdto import UserCreate

router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Inject service

db_dep= Annotated[Session, Depends(get_db)]
token_dep = Annotated[str, Depends(oauth2_scheme)]
form_dep = Annotated[OAuth2PasswordRequestForm, Depends()]

@router.post("/register")
def register_user(
    user: UserCreate,
    db: db_dep
):
    return create_user(user,db)

@router.post("/login")
def login_user(
        db: db_dep,
        form_data: form_dep,
):
    result = login(form_data.username, form_data.password, db)
    if not result:
        raise HTTPException(400, "Invalid username or password")
    return result

@router.get("/me")
def get_current_user(
    token: token_dep,
    db: db_dep,
):
    return get_current_user_by_token(token,db)


from fastapi import status, Body
import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class TokenRequest(BaseModel):
    refresh_token: str

@router.post("/refresh")
def refresh_token(
    token_data: TokenRequest,
    db: Session = Depends(get_db),
):
    try:
        logger.info("Refresh token request received")
        
        # Get the token from the request model
        token = token_data.refresh_token.strip()
        logger.info(f"Token received: {token[:10]}...")
        
        if not token:
            logger.error("Empty token provided")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "invalid_token", "message": "Token cannot be empty"}
            )
        
        try:
            # Decode the token
            logger.info("Decoding token...")
            payload = jwt_decode(token)
            logger.info("Token decoded successfully")
            
            # Extract user information
            user_id = payload.get("id")
            username = payload.get("sub")
            role = payload.get("role")
            
            if not all([user_id, username, role]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"error": "invalid_token", "message": "Token is missing required fields"}
                )
            
            # Create new tokens
            new_payload = {
                "sub": username,
                "id": user_id,
                "role": role
            }
            
            # Generate new access token but keep the same refresh token
            new_access_token = create_access_token(new_payload)
            
            logger.info("New access token generated successfully")
            
            return {
                "access_token": new_access_token,
                "refresh_token": token,  # Return the same refresh token
                "token_type": "bearer"
            }
            
        except HTTPException as e:
            logger.error(f"Token validation error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": "invalid_token", "message": "Invalid or expired refresh token"}
            )
            
        # Decode the refresh token
        try:
            logger.info(f"Attempting to decode token: {token}")
            payload = jwt_decode(token)
            logger.info(f"Token decoded successfully: {payload}")
        except HTTPException as e:
            logger.error(f"Token validation error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected token decode error: {str(e)}\n{traceback.format_exc()}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "error": "invalid_token",
                    "message": "Invalid or expired refresh token"
                },
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Validate required fields in the token
        required_fields = ["id", "sub", "role"]
        for field in required_fields:
            if field not in payload:
                logger.error(f"Missing required field in token: {field}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "error": "invalid_token",
                        "message": f"Invalid token: missing required field '{field}'"
                    }
                )
        
        # Extract user information from the refresh token
        try:
            user_id = int(payload["id"])
            username = str(payload["sub"])
            role = str(payload["role"])
            
            logger.info(f"User info - ID: {user_id}, Username: {username}, Role: {role}")
            
            # Create new tokens
            new_payload = {
                "sub": username,
                "id": user_id,
                "role": role
            }
            
            # Generate new access token
            new_access_token = create_access_token(new_payload)
            logger.info("New access token generated")
            
            # Generate new refresh token
            new_refresh_token = create_refresh_token(new_payload)
            logger.info("New refresh token generated")
            
            return {
                "access_token": new_access_token,
                "refresh_token": new_refresh_token,
                "token_type": "bearer"
            }
            
        except Exception as e:
            logger.error(f"Error in token generation: {str(e)}\n{traceback.format_exc()}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "token_generation_failed",
                    "message": "Failed to generate new tokens"
                }
            )
            
    except HTTPException as e:
        # Re-raise HTTP exceptions with their original status codes
        logger.error(f"HTTP Exception: {str(e)}")
        raise
        
    except Exception as e:
        # Log the full traceback for unexpected errors
        error_msg = f"Unexpected error in refresh_token: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        
        # Return a generic error message to the client
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "internal_server_error",
                "message": "An unexpected error occurred while processing your request"
            }
        )

#
# @router.post("/login")
# def login_user(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     service: UserService = Depends(get_user_service)
# ):
#     result = service.login(form_data.username, form_data.password)
#
#     if not result:
#         raise HTTPException(400, "Invalid username or password")
#
#     return result
# #return all  user if curr is admin
# @router.get("/users")
# def get_all_users(
#     token: str = Depends(oauth2_scheme),
#     service: UserService = Depends(get_user_service)
# ):
#     return service.get_all_users(token)
#
#
# @router.get("/auth/me")
# def get_current_user(
#     token: str = Depends(oauth2_scheme),
#     service: UserService = Depends(get_user_service)
# ):
#     return service.get_current_user(token)
