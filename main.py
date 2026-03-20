"""Simple todo list API."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from todos.service import TodoService

app = FastAPI(title="Todo Service")
svc = TodoService()


class CreateRequest(BaseModel):
    title: str
    priority: str = "medium"


@app.post("/todos")
def create(req: CreateRequest):
    return svc.create(req.title, req.priority).__dict__


@app.get("/todos")
def list_todos():
    return [t.__dict__ for t in svc.list_all()]


@app.post("/todos/{todo_id}/complete")
def complete(todo_id: int):
    todo = svc.complete(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo.__dict__


@app.delete("/todos/{todo_id}")
def delete(todo_id: int):
    if not svc.delete(todo_id):
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"deleted": todo_id}


@app.get("/health")
def health():
    return {"status": "ok"}
