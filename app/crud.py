from bson import ObjectId
from app.utils import normalize_mongo_document


async def create_todo(todo: dict, db):
    result = await db.todos.insert_one(todo)
    return str(result.inserted_id)


async def get_todos(db):
    todos = []
    cursor = db.todos.find({})
    async for doc in cursor:
        todos.append(normalize_mongo_document(doc))
    return todos


async def get_todo_by_id(id: str, db):
    doc = await db.todos.find_one({"_id": ObjectId(id)})
    if doc:
        return normalize_mongo_document(doc)
    return None


async def delete_todo_by_id(id: str, db):
    result = await db.todos.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0
