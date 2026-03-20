"""Todo service — manages a simple in-memory todo list."""

from typing import Optional
from todos.models import Todo


class TodoService:
    def __init__(self):
        self._todos: dict[int, Todo] = {}
        self._next_id: int = 1

    def create(self, title: str, priority: str = "medium") -> Todo:
        todo = Todo(id=self._next_id, title=title, priority=priority)
        self._todos[self._next_id] = todo
        self._next_id += 1
        return todo

    def get(self, todo_id: int) -> Optional[Todo]:
        return self._todos.get(todo_id)

    def list_all(self) -> list[Todo]:
        return list(self._todos.values())

    def complete(self, todo_id: int) -> Optional[Todo]:
        """Mark a todo as completed."""
        todo = self.get(todo_id)
        if todo is None:
            return None
        todo.completed = True
        return todo

    def delete(self, todo_id: int) -> bool:
        if todo_id in self._todos:
            del self._todos[todo_id]
            return True
        return False

    def pending(self) -> list[Todo]:
        return [t for t in self._todos.values() if not t.completed]

    def completed(self) -> list[Todo]:
        return [t for t in self._todos.values() if t.completed]
