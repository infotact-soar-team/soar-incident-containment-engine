from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.logging_config import logger


async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error on {request.method} {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": "Something went wrong. This has been logged for review.",
        },
    )