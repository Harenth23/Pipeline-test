from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_create_and_get_todo():
    todo = {"title": "Test Todo", "description": "Write test", "completed": False}
    response = client.post("/todos/", json=todo)
    assert response.status_code == 200
    todo_id = response.json()["id"]

    get_response = client.get(f"/todos/{todo_id}")
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Test Todo"
