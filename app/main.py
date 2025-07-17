from fastapi import FastAPI, HTTPException, Depends
from app.models import Todo
from app.crud import create_todo, get_todos, get_todo_by_id, delete_todo_by_id
from app.database import get_db

app = FastAPI()


@app.post("/todos/")
async def add_todo(todo: Todo, db=Depends(get_db)):
    todo_id = await create_todo(todo.model_dump(), db)
    return {"id": todo_id}

@app.get("/todo/")
async def read_todos(db=Depends(get_db)):
    return await get_todos(db)    

@app.get("/todos/{id}")
async def read_todo(id: str, db=Depends(get_db)):
    todo = await get_todo_by_id(id, db)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.delete("/todos/{id}")
async def delete_todo(id: str, db=Depends(get_db)):
    deleted = await delete_todo_by_id(id, db)
    if deleted:
        return {"message": "Deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")
