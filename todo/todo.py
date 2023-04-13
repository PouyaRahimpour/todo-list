from typing import Any, Dict, NamedTuple, List, Optional

from pathlib import Path
from todo import DB_READ_ERROR, ID_ERROR

from todo.database import DatabaseHandler
from todo.task import Task
from todo.linked_list import LinkedList


class CurrentTodo(NamedTuple):
    todo: Task
    error: int


class Todoer:
    def __init__(self, db_path: Path) -> None:
        self._dbhandler = DatabaseHandler(db_path)

    def add(self, task: Task) -> CurrentTodo:

        todo = {
            "Name": task.name,
            "Priority": task.priority.name,
            "Done": False,
            "Note": task.note,
            "Steps": task.steps,
            "CreatedDate": task.created_date,
            "DueDate": task.due_date,
            "Tags": task.tags
        }
        read = self._dbhandler.read_todos()
        if read.error == DB_READ_ERROR:
            return CurrentTodo(task, read.error)

        read.todo_list.add_last(todo)
        write = self._dbhandler.write_todos(read.todo_list)
        return CurrentTodo(task, write.error)

    def get_todo_list(self, tag: Optional[str]) -> LinkedList:
        todo_list, error = self._dbhandler.read_todos()
        if tag is not None:
            for todo in todo_list:
                found = False
                for t in todo["Tags"]:
                    if t == tag:
                        found = True
                        break
                if not found:
                    todo_list.remove_node_with_data(todo)

        return todo_list

    def set_done(self, todo_id: int) -> CurrentTodo:
        read = self._dbhandler.read_todos()
        if read.error:
            return CurrentTodo({}, read.error)
        try:
            todo = read.todo_list[todo_id - 1]
        except IndexError:
            return CurrentTodo({}, ID_ERROR)
        todo["Done"] = True
        write = self._dbhandler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)

    def remove(self, todo_id: int) -> CurrentTodo:
        read = self._dbhandler.read_todos()
        if read.error:
            return CurrentTodo({}, read.error)
        try:
            todo = read.todo_list.remove_node(todo_id - 1)
        except IndexError:
            return CurrentTodo({}, ID_ERROR)
        write = self._dbhandler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)

    def remove_all(self) -> CurrentTodo:
        write = self._dbhandler.write_todos([])
        return CurrentTodo({}, write.error)

    def change_todo(self, todo_id: int, task: Task) -> CurrentTodo:
        read = self._dbhandler.read_todos()
        if read.error:
            return CurrentTodo({}, read.error)
        try:
            todo = read.todo_list[todo_id - 1]
        except IndexError:
            return CurrentTodo({}, ID_ERROR)
        if task.name is not None:
            todo["Name"] = task.name
        if task.priority is not None:
            todo["Priority"] = task.priority
        if task.done is not None:
            todo["Done"] = task.done
        if task.note is not None:
            todo["Note"] = task.note
        if task.created_date is not None:
            todo["CreatedDate"] = task.created_date
        if task.due_date is not None:
            todo["DueDate"] = task.due_date
        if task.steps is not None:
            todo["Steps"] = task.steps
        if task.tags is not None:
            todo["Tags"] = task.tags

        write = self._dbhandler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)

    def _make_str():
        pass
