from fastapi import FastAPI, HTTPException
from app.models import Todo
from app.crud import create_todo, get_todos, get_todo_by_id, delete_todo_by_id

app = FastAPI()

@app.post("/todos/")
async def add_todo(todo: Todo):
    todo_id = await create_todo(todo.dict())
    return {"id": todo_id}

@app.get("/todos/")
async def read_todos():
    return await get_todos()

@app.get("/todos/{id}")
async def read_todo(id: str):
    todo = await get_todo_by_id(id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.delete("/todos/{id}")
async def delete_todo(id: str):
    deleted = await delete_todo_by_id(id)
    if deleted:
        return {"message": "Deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")
