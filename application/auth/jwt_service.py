from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from fastapi import HTTPException, status, Depends
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from application.auth.jwt_config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from infrastructure.db.base import get_db
from infrastructure.repositories.user_repository import user_repo






def create_access_token(data: dict, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode["exp"] = expire

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_days: int = REFRESH_TOKEN_EXPIRE_DAYS):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=expires_days)
    to_encode["exp"] = expire

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def jwt_decode(token: str):
    if not token:
        raise HTTPException(status_code=401, detail="No token provided")
        
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Check if token is expired
        if "exp" in payload and payload["exp"] < datetime.utcnow().timestamp():

            raise HTTPException(status_code=403, detail="Token has expired")
            
        return payload
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token has expired")
    except jwt.JWTClaimsError:
        raise HTTPException(status_code=403, detail="Invalid token claims")
    except jwt.JWTError as e:
        raise HTTPException(status_code=403, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error decoding token")


# async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#
#     try:
#         if not token:
#             raise credentials_exception
#
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#
#         # Check if token is expired
#         if "exp" in payload and payload["exp"] < datetime.utcnow().timestamp():
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Token has expired",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
#
#         user_id: int = int(payload.get("id"))
#         if user_id is None:
#             raise credentials_exception
#
#         user = user_repo['get_by_id'](db, user_id)
#         if user is None:
#             raise credentials_exception
#
#         return user
#
#     except (JWTError, ValueError):
#         raise credentials_exception
#     except jwt.JWTClaimsError:
#         raise HTTPException(status_code=403, detail="Invalid token claims")
#     except jwt.JWTError as e:
#         raise HTTPException(status_code=403, detail="Invalid token")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Error decoding token")