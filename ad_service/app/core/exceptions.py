import logging
from datetime import UTC, datetime
from typing import Any

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


def _utc_timestamp() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _normalize_detail(detail: Any) -> str:
    if detail is None:
        return "Request could not be processed."
    if isinstance(detail, str):
        return detail
    if isinstance(detail, list | dict):
        return str(detail)
    return str(detail)


def error_response(status_code: int, message: str, path: str) -> dict[str, Any]:
    return {
        "timestamp": _utc_timestamp(),
        "status": status_code,
        "message": message,
        "path": path,
    }


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    message = _normalize_detail(exc.detail)
    body = error_response(exc.status_code, message, request.url.path)
    return JSONResponse(status_code=exc.status_code, content=body)


def _validation_message(errors: list[Any]) -> str:
    if not errors:
        return "Request validation failed."
    parts: list[str] = []
    for err in errors[:5]:
        if not isinstance(err, dict):
            parts.append(str(err))
            continue
        loc = err.get("loc", ())
        loc_str = ".".join(str(x) for x in loc if x != "body")
        msg = err.get("msg", "invalid")
        parts.append(f"{loc_str or 'request'}: {msg}")
    suffix = f" (+{len(errors) - 5} more)" if len(errors) > 5 else ""
    return "Validation failed: " + "; ".join(parts) + suffix


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = _validation_message(exc.errors())
    body = error_response(code, message, request.url.path)
    return JSONResponse(status_code=code, content=body)


async def integrity_exception_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    error_text = str(exc.orig) if exc.orig else str(exc)
    lowered = error_text.lower()

    if "foreignkeyviolationerror" in lowered or "foreign key" in lowered:
        message = "Related entity does not exist. Check provided IDs."
    elif "uniqueviolationerror" in lowered or "unique" in lowered:
        message = "A record with the same unique value already exists."
    else:
        message = "Database integrity constraint was violated."

    code = status.HTTP_400_BAD_REQUEST
    body = error_response(code, message, request.url.path)
    logger.warning("IntegrityError on %s: %s", request.url.path, error_text)
    return JSONResponse(status_code=code, content=body)


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "An unexpected error occurred. Please try again later."
    body = error_response(code, message, request.url.path)
    logger.exception("Unhandled error on %s", request.url.path)
    return JSONResponse(status_code=code, content=body)
