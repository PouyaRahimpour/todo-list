import configparser

from pathlib import Path

import json

from typing import Any, Dict, List, NamedTuple


from todo import DB_WRITE_ERROR, SUCCESS, DB_READ_ERROR, JSON_ERROR
from todo.linked_list import LinkedList

DEFAULT_DB_PATH = Path.home().joinpath(
    "." + Path.home().stem + "_todo.json"
)

def get_database_path(config_file: Path) -> Path:
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])

def init_database(db_path: Path) -> int:
    try:
        db_path.write_text("[]")
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR

class DBResponse(NamedTuple):
    todo_list: LinkedList
    error : int

class DatabaseHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def read_todos(self) -> DBResponse:
        try:
            with self._db_path.open("r") as db:
                try:
                    return DBResponse(LinkedList(json.load(db)), SUCCESS)
                except json.JSONDecodeError:
                    return DBResponse(LinkedList(), JSON_ERROR)
        except OSError:
            return DBResponse(LinkedList(), DB_READ_ERROR)
    
    def write_todos(self, todo_list: LinkedList) -> DBResponse:
        try:
            with self._db_path.open("w") as db:
                json.dump(list(todo_list), db, indent=4)
            return DBResponse(todo_list, SUCCESS)
        except OSError:
            return DBResponse(todo_list, DB_WRITE_ERROR)
