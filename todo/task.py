from datetime import datetime

from enum import Enum


class Priority(Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3


class Task:

    def __init__(self, name: str, priority: Priority = Priority.MEDIUM, due_date: str = "", note: str = "", steps: list[str] = [], tags: list[str] = []):
        self.name = name
        self.steps = steps
        self.tags = tags
        self.priority = priority
        self.due_date = due_date
        self.note = note
        self.created_date = str(datetime.date(datetime.now()))
        self.done = False

    def __repr__(self) -> str:
        return f"Task({self.name}, priority={self.priority.name}, due_date={str(self.due_date)}, note={self.note}, steps={str(self.steps)}, tags={str(self.tags)}"
