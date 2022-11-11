from typing import Any, Dict, NamedTuple, List

from pathlib import Path
from todo import DB_READ_ERROR, ID_ERROR

from todo.database import DatabaseHandler
from task import Task
class CurrentTodo(NamedTuple):
    todo: Dict[str, Any]
    error: int

class Todoer:
    def __init__(self, db_path: Path) -> None:
        self._dbhandler = DatabaseHandler(db_path)
    
    def add(self, task: Task) -> CurrentTodo:
       
        todo = {
            "Description": task.note,
            "Priority": task.priority,
            "Done": False,
        }
        read = self._dbhandler.read_todos()
        if read.error == DB_READ_ERROR:
            return CurrentTodo(todo, read.error)

        read.todo_list.append(todo)
        write = self._dbhandler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)

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