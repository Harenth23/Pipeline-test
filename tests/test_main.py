import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
import asyncio

client = TestClient(app)

@pytest.fixture(scope="module")
def event_loop():
    # To avoid 'RuntimeError: This event loop is already running'
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(autouse=True)
async def clear_todos():
    """Cleanup MongoDB todos collection before each test."""
    db = get_db()
    await db.todos.delete_many({})
    yield
    await db.todos.delete_many({})


def test_create_and_get_todo():
    todo = {
        "title": "Test Todo",
        "description": "Write test",
        "completed": False
    }

    # Create Todo
    response = client.post("/todos/", json=todo)
    assert response.status_code == 200
    todo_id = response.json()["id"]
    assert isinstance(todo_id, str)

    # Get Todo by ID
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["description"] == "Write test"
    assert data["completed"] is False

    # Get all Todos
    response = client.get("/todos/")
    assert response.status_code == 200
    todos = response.json()
    assert len(todos) == 1
    assert todos[0]["title"] == "Test Todo"
