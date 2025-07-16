from app.main import app
from fastapi.testclient import TestClient
import mongomock
from unittest.mock import AsyncMock, patch

client = TestClient(app)

@patch("app.crud.db.todos.insert_one", new_callable=AsyncMock)
def test_create_and_get_todo(mock_insert):
    mock_insert.return_value = type("obj", (object,), {"inserted_id": "12345"})

    todo = {"title": "Test Todo", "description": "Write test", "completed": False}
    response = client.post("/todos/", json=todo)

    assert response.status_code == 200
