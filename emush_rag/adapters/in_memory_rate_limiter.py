from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Protocol

from emush_rag.ports.rate_limiter import RateLimiter


class DateTimeProvider(Protocol):
    """Protocol for datetime providers"""

    def now(self) -> datetime: ...


class InMemoryRateLimiter(RateLimiter):
    """In-memory implementation of rate limiting"""

    def __init__(
        self, max_requests: int = 5, window_seconds: int = 60, datetime_provider: DateTimeProvider = datetime
    ):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, List[datetime]] = defaultdict(list)
        self.datetime = datetime_provider

    def _clean_old_requests(self, client_id: str) -> None:
        """Clean up old requests outside the current window"""
        now = self.datetime.now()
        window_start = now - timedelta(seconds=self.window_seconds)
        self.requests[client_id] = [ts for ts in self.requests[client_id] if ts > window_start]

    def is_allowed(self, client_id: str) -> bool:
        """Check if a request from the given client is allowed"""
        self._clean_old_requests(client_id)
        return len(self.requests[client_id]) < self.max_requests

    def record_request(self, client_id: str) -> None:
        """Record a request from the given client"""
        self._clean_old_requests(client_id)
        self.requests[client_id].append(self.datetime.now())
