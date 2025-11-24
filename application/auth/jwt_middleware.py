
from fastapi.responses import JSONResponse
from jose import JWTError
from starlette.middleware.base import BaseHTTPMiddleware

from fastapi import Depends, HTTPException, Request
from presentation.auth_router import oauth2_scheme
from application.auth.jwt_service import jwt_decode


class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):

        request.state.user_id = None
        request.state.role = None
        request.state.username = None

        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split("Bearer ")[1]

            try:
                payload = jwt_decode(token)

                request.state.user_id = payload.get("id")
                request.state.role = payload.get("role")
                request.state.username = payload.get("sub")

                if request.state.user_id is None:
                    return JSONResponse(
                        status_code=401,
                        content={"detail": "Invalid token"},
                    )

            except HTTPException as e:
                return JSONResponse(
                    status_code=e.status_code,
                    content={"detail": e.detail},
                )

            except JWTError:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid token"},
                )

        return await call_next(request)

def admin_or_employee(token: str = Depends(oauth2_scheme)):
    payload = jwt_decode(token)
    role = payload.get("role")

    if role not in ["ADMIN", "EMPLOYEE"] :
        raise HTTPException(status_code=403, detail="Not authorized")

    return payload
def admin_or_employee_or_user(
    request: Request,
    token: str = Depends(oauth2_scheme)
):
    payload = jwt_decode(token)
    role = payload.get("role")
    user_id = payload.get("id")

    path_id = int(request.path_params.get("id"))

    if role in ["ADMIN", "EMPLOYEE"]:
        return payload

    if role == "USER" and user_id == path_id:
        return payload

    raise HTTPException(status_code=403, detail="Not authorized")

def auther(
           token :str = Depends(oauth2_scheme)
):
    payload = jwt_decode(token)
    role = payload.get("role")
    if role == "AUTHOR":
        return payload


    raise HTTPException(status_code=403, detail="Not authorized only author")

def user_role(token: str = Depends(oauth2_scheme)):
    payload = jwt_decode(token)
    role = payload.get("role")
    if role == "USER":
        return payload

    raise HTTPException(status_code=403, detail="Not authorized only user")