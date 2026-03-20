from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Todo:
    id: int
    title: str
    completed: bool = False
    priority: str = "medium"  # low / medium / high
