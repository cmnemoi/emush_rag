from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from emush_rag import __version__
from emush_rag.api.dependencies import rate_limiter
from emush_rag.api.main import answer_user_question, app
from emush_rag.api.middleware import RateLimitMiddleware
from tests.test_doubles import fake_answer_user_question
from tests.test_doubles.fake_datetime import FakeDateTime

client = TestClient(app)


@pytest.fixture
def fake_datetime_provider():
    """Provide a fake datetime for controlled time advancement"""
    return FakeDateTime(datetime(2024, 1, 1))


@pytest.fixture
def test_rate_limiter(fake_datetime_provider):
    """Provide a rate limiter with controlled datetime"""
    return rate_limiter(datetime_provider=fake_datetime_provider)


@pytest.fixture
def setup_api(test_rate_limiter):
    """Setup middleware and dependency overrides for tests"""
    # Clear existing middlewares
    app.user_middleware = []
    app.middleware_stack = None
    app.add_middleware(RateLimitMiddleware, rate_limiter=test_rate_limiter)

    # Setup dependency overrides
    app.dependency_overrides[answer_user_question] = fake_answer_user_question

    yield

    # Cleanup
    app.dependency_overrides = {}


def test_main():
    response = client.get("/")
    assert response.status_code == 200


def test_rate_limiting(setup_api, fake_datetime_provider: FakeDateTime):
    """Test that the API enforces rate limiting"""
    # Should allow 100 requests per minute
    for _ in range(100):
        response = client.post("/api/questions", json={"question": "What is eMush?", "chat_history": []})
        assert response.status_code == 200

    # The next request should be rate limited
    response = client.post("/api/questions", json={"question": "What is eMush?", "chat_history": []})
    assert response.status_code == 429
    assert "Too many requests" in response.json()["detail"]

    # Advance time by 60 seconds to reset the rate limit window
    fake_datetime_provider.advance(60)

    # Should be able to make requests again
    response = client.post("/api/questions", json={"question": "What is eMush?", "chat_history": []})
    assert response.status_code == 200
    assert "answer" in response.json()


def test_version_endpoint():
    response = client.get("/api/version")
    assert response.status_code == 200
    assert response.json() == {"version": __version__}


def test_questions_endpoint(setup_api):
    """Test that the questions endpoint returns a valid response"""
    response = client.post("/api/questions", json={"question": "What is eMush?", "chat_history": []})
    assert response.status_code == 200
