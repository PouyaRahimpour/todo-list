from typing import Any, Dict, NamedTuple, List

from pathlib import Path
from todo import DB_READ_ERROR, ID_ERROR

from todo.database import DatabaseHandler
from todo.task import Task
class CurrentTodo(NamedTuple):
    todo: Task
    error: int

class Todoer:
    def __init__(self, db_path: Path) -> None:
        self._dbhandler = DatabaseHandler(db_path)
    
    def add(self, task: Task) -> CurrentTodo:
       
        todo = {
            "Description": task.note,
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
        print(read.todo_list)
        write = self._dbhandler.write_todos(read.todo_list)
        return CurrentTodo(task, write.error)

    def get_todo_list(self) -> List[Dict[str, Any]]:
        read = self._dbhandler.read_todos()
        return read.todo_list

    def get_todo_list(self) -> List[Dict[str, Any]]:
        read = self._dbhandler.read_todos()
        return read.todo_list
    
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
            todo = read.todo_list.pop(todo_id - 1)
        except IndexError:
            return CurrentTodo({}, ID_ERROR)
        write = self._dbhandler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)

    def remove_all(self) -> CurrentTodo:
        write = self._dbhandler.write_todos([])
        return CurrentTodo({}, write.error)

    def _make_str():
        pass