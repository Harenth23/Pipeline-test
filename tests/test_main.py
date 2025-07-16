from app.main import app
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

client = TestClient(app)

def test_create_and_get_todo(monkeypatch):
    fake_insert = MagicMock(return_value={"inserted_id": "12345"})
    monkeypatch.setattr("app.crud.db.todos.insert_one", fake_insert)

    todo = {"title": "Test", "description": "Desc", "completed": False}
    response = client.post("/todos/", json=todo)

    assert response.status_code == 200
