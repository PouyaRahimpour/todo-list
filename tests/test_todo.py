from typer.testing import CliRunner

import json
import pytest
from typer.testing import CliRunner

from todo import (
    DB_READ_ERROR, 
    SUCCESS, 
    __app_name__, 
    __version__,
    cli,
    todo,
)

runner = CliRunner()

def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout

@pytest.fixture
def mock_json_file(tmp_path):
    todo = [{"Description": "go to DS class", "Priority": 2, "Done": False}]
    db_file = tmp_path/"todo.json"
    with db_file.open("w") as db:
        json.dump(todo, db, indent=4)
    return db_file
    
test_data1 = {
    "description": ["Study", "for", "probability", "exam"],
    "priority": 1,
    "todo": {
        "Description": "Study for probability exam.",
        "Priority": 1,
        "Done": False,
    },
}
test_data2 = {
    "description": ["Bake", "a", "cake"],
    "priority": 3,
    "todo": {
        "Description": "Bake a cake.",
        "Priority": 3,
        "Done": False,
    },
}

@pytest.mark.parametrize(
    "description, priority, expected",
    [
        pytest.param(
            test_data1["description"],
            test_data1["priority"],
            (test_data1["todo"], SUCCESS),
        ),
        pytest.param(
            test_data2["description"],
            test_data2["priority"],
            (test_data2["todo"], SUCCESS),
        ),
    ],
)
def test_add(mock_json_file, description, priority, expected):
    todoer = todo.Todoer(mock_json_file)
    assert todoer.add(description, priority) == expected
    read = todoer._dbhandler.read_todos()
    assert len(read.todo_list) == 2