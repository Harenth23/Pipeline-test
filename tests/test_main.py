import pytest
import pytest_asyncio
import asyncio 
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import get_db
from motor.motor_asyncio import AsyncIOMotorClient

@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(autouse=True)
async def clear_todos():
    db = get_db()
    await db.todos.delete_many({})
    yield
    await db.todos.delete_many({})

@pytest.mark.asyncio
async def test_create_and_get_todo():
    todo = {
        "title": "Test Todo",
        "description": "Write test",
        "completed": False
    }

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:    
        # Create Todo
        response = await client.post("/todos/", json=todo)
        assert response.status_code == 200
        todo_id = response.json()["id"]
        assert isinstance(todo_id, str)

        # Get Todo by ID
        response = await client.get(f"/todos/{todo_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Todo"
        assert data["description"] == "Write test"
        assert data["completed"] is False

        # Get all Todos
        response = await client.get("/todos/")
        assert response.status_code == 200
        todos = response.json()
        assert any(t["id"] == todo_id for t in todos)
        matching = next(t for t in todos if t["id"] == todo_id)
        assert matching["title"] == "Test Todo"

    # Optional: Cleanup the inserted test data
    await db.todos.delete_one({"_id": todo_id})
