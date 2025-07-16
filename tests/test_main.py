from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from app.main import app

client = TestClient(app)

@patch("app.database.get_db")
def test_create_and_get_todo(mock_get_db):
    # Setup mock database and collection
    mock_todos = MagicMock()
    mock_todos.insert_one = AsyncMock(return_value=MagicMock(inserted_id="12345"))

    mock_db = MagicMock()
    mock_db.todos = mock_todos

    # Mock get_db() to return the fake db
    mock_get_db.return_value = mock_db

    todo = {"title": "Test Todo", "description": "Write test", "completed": False}
    response = client.post("/todos/", json=todo)

    assert response.status_code == 200
    assert response.json() == {"id": "12345"}
