from fastapi.testclient import TestClient

from emush_rag.api.main import app

client = TestClient(app)


def test_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_questions_endpoint():
    response = client.post("/api/questions", json={"question": "What is eMush?", "chat_history": []})
    assert response.status_code == 200
