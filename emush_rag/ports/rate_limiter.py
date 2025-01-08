from abc import ABC, abstractmethod


class RateLimiter(ABC):
    """Port for rate limiting functionality"""

    @abstractmethod
    def is_allowed(self, client_id: str) -> bool:
        """Check if a request from the given client is allowed"""
        pass

    @abstractmethod
    def record_request(self, client_id: str) -> None:
        """Record a request from the given client"""
        pass
