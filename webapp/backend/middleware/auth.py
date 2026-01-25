"""
Simple token-based authentication middleware.

This middleware checks for an access token in the URL query parameters.
If ACCESS_TOKEN environment variable is set, all requests must include
the token as a query parameter: ?token=YOUR_TOKEN

The health endpoint is always accessible without authentication.
"""
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from core.config import ACCESS_TOKEN


class TokenAuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware to enforce token-based authentication via query parameters.
    
    If ACCESS_TOKEN is configured, requests must include ?token=ACCESS_TOKEN
    The /health endpoint is exempt from authentication.
    """
    
    async def dispatch(self, request: Request, call_next):
        # If no ACCESS_TOKEN is configured, allow all requests
        if ACCESS_TOKEN is None:
            return await call_next(request)
        
        # Always allow access to health endpoint without token
        if request.url.path == "/health":
            return await call_next(request)
        
        # Check for token in query parameters
        token = request.query_params.get("token")
        
        if token != ACCESS_TOKEN:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "detail": "Access denied. Valid token required."
                }
            )
        
        return await call_next(request)
