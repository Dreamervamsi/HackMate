from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import logging
import time
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware for global error handling and consistent error responses"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException as http_exc:
            # Handle HTTP exceptions
            logger.warning(f"HTTP Exception: {http_exc.status_code} - {http_exc.detail}")
            
            error_response = {
                "status": "error",
                "detail": http_exc.detail,
                "error_code": f"HTTP_{http_exc.status_code}",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            return JSONResponse(
                status_code=http_exc.status_code,
                content=error_response
            )
        except ValueError as val_exc:
            # Handle validation errors
            logger.warning(f"Validation Error: {val_exc}")
            
            error_response = {
                "status": "error",
                "detail": str(val_exc),
                "error_code": "VALIDATION_ERROR",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=error_response
            )
        except Exception as exc:
            # Handle unexpected errors
            logger.error(f"Unexpected Error: {exc}", exc_info=True)
            
            error_response = {
                "status": "error",
                "detail": "An unexpected error occurred",
                "error_code": "INTERNAL_ERROR",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=error_response
            )


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and responses"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request details
        logger.info(f"Incoming request: {request.method} {request.url.path}")
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        
        # Log response details
        logger.info(
            f"Request completed: {request.method} {request.url.path} "
            f"- Status: {response.status_code} - Time: {process_time:.3f}s"
        )
        
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware for adding security headers to responses"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response