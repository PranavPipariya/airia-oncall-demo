"""Tests for the todo service."""

import pytest
from todos.service import TodoService


@pytest.fixture
def svc():
    return TodoService()


# ── Create / list (all pass) ──────────────────────────────────────────────────

def test_create_todo(svc):
    todo = svc.create("Buy milk")
    assert todo.id == 1
    assert todo.title == "Buy milk"
    assert todo.completed is False


def test_list_empty(svc):
    assert svc.list_all() == []


def test_list_todos(svc):
    svc.create("Task A")
    svc.create("Task B")
    assert len(svc.list_all()) == 2


# ── Complete (FAILING due to bug) ─────────────────────────────────────────────

def test_complete_marks_as_done(svc):
    """Completing a todo must set completed=True."""
    todo = svc.create("Write tests")
    result = svc.complete(todo.id)
    # BUG: not todo.completed  →  False → True first time (passes)
    # but semantics are wrong; second call reverts it
    assert result.completed is True


def test_complete_is_idempotent(svc):
    """Completing an already-completed todo should keep it completed."""
    todo = svc.create("Deploy to prod")
    svc.complete(todo.id)   # first call: False → True
    svc.complete(todo.id)   # BUG: second call: True → False
    assert svc.get(todo.id).completed is True


def test_completed_list_accurate(svc):
    """completed() must return only truly completed todos."""
    svc.create("Alpha")
    svc.create("Beta")
    svc.complete(1)
    assert len(svc.completed()) == 1
    assert svc.completed()[0].id == 1


def test_pending_list_accurate(svc):
    """pending() must not include completed todos."""
    svc.create("Alpha")
    svc.create("Beta")
    svc.complete(1)
    pending = svc.pending()
    assert len(pending) == 1
    assert pending[0].id == 2


# ── Delete (all pass) ─────────────────────────────────────────────────────────

def test_delete_todo(svc):
    todo = svc.create("Temporary")
    assert svc.delete(todo.id) is True
    assert svc.get(todo.id) is None


def test_delete_nonexistent(svc):
    assert svc.delete(999) is False
