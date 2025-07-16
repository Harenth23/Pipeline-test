from bson import ObjectId
from app.database import get_db

async def create_todo(todo):
    db = get_db()
    result = await db.todos.insert_one(todo)
    return str(result.inserted_id)


async def get_todos():
    todos = await db.todos.find().to_list(100)
    for todo in todos:
        todo["_id"] = str(todo["_id"])
    return todos


async def get_todo_by_id(id: str):
    todo = await db.todos.find_one({"_id": ObjectId(id)})
    if todo:
        todo["_id"] = str(todo["_id"])
    return todo


async def delete_todo_by_id(id: str):
    result = await db.todos.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0
