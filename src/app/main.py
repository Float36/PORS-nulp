from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.app.api.v1 import ads, users, chats
from src.app.core.config import settings

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from src.app.core.exceptions import http_exception_handler, validation_exception_handler

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(ads.router, prefix=settings.API_V1_STR, tags=["Ads"])
app.include_router(users.router, prefix=settings.API_V1_STR, tags=["Users"])

app.include_router(chats.router, prefix=settings.API_V1_STR, tags=["Chats"])


app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

@app.get("/")
def root():
    return {"message": "Welcome to Lost&Found API. Go to /docs for Swagger."}