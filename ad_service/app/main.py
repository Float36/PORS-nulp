import logging

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware

from app.api.v1 import ads, categories, chats, messages, photos
from app.core.config import settings
from app.core.exceptions import (
    http_exception_handler,
    integrity_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ads.router, prefix=settings.API_V1_STR, tags=["Ads"])
app.include_router(chats.router, prefix=settings.API_V1_STR, tags=["Chats"])
app.include_router(categories.router, prefix=settings.API_V1_STR, tags=["Categories"])
app.include_router(photos.router, prefix=settings.API_V1_STR, tags=["Photos"])
app.include_router(messages.router, prefix=settings.API_V1_STR, tags=["Messages"])

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(IntegrityError, integrity_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)


@app.get("/")
def root():
    return {"message": "Lost&Found Ad Service. Open /docs for Swagger."}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
