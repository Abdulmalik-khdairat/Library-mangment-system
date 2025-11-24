from fastapi import FastAPI, Depends, HTTPException, status


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



