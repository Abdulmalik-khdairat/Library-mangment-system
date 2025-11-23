from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles

from application.auth.jwt_middleware import JWTMiddleware
from presentation.auth_router import router as auth_router
from presentation.user_router import router as user_router
from presentation.book_router import router as book_router
from presentation.Borrow_router import router as borrow_router

app = FastAPI()
app.add_middleware(JWTMiddleware)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(borrow_router)
app.include_router(book_router)



