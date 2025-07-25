from http import HTTPStatus

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from emush_rag.ports.rate_limiter import RateLimiter


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for rate limiting requests"""

    def __init__(self, app, rate_limiter: RateLimiter):
        super().__init__(app)
        self.rate_limiter = rate_limiter

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path == "/api/questions":
            client_id = request.client.host  # type: ignore
            if not self.rate_limiter.is_allowed(client_id):
                return Response(
                    content='{"detail": "Too many requests"}',
                    status_code=HTTPStatus.TOO_MANY_REQUESTS,
                    media_type="application/json",
                )
            self.rate_limiter.record_request(client_id)

        response = await call_next(request)
        return response
