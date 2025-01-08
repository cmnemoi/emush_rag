from fastapi.testclient import TestClient

from emush_rag import __version__
from emush_rag.api.main import answer_user_question, app
from tests.test_doubles import fake_answer_user_question

client = TestClient(app)


def test_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_version_endpoint():
    response = client.get("/api/version")
    assert response.status_code == 200
    assert response.json() == {"version": __version__}


def test_questions_endpoint():
    app.dependency_overrides[answer_user_question] = fake_answer_user_question

    response = client.post("/api/questions", json={"question": "What is eMush?", "chat_history": []})
    assert response.status_code == 200
