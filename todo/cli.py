
from typing import Optional, List

import typer
from todo.task import Task, Priority

from todo import (
    __app_name__, __version__, ERRORS, config, database, todo
)

from pathlib import Path


app = typer.Typer()

@app.command()
def init(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_PATH), 
        "--db-path",
        "-db",
        prompt="todo database location?"
    ),
) -> None:
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg = typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg = typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The todo database is {db_path}", fg=typer.colors.GREEN)
    

def get_todoer() -> todo.Todoer:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not found, Plese, run "todo init"',
            fg = typer.colors.RED,
        )
        raise typer.Exit(1)

    if db_path.exists():
        return todo.Todoer(db_path)
    else:
        typer.secho(
            'Database not found. Please, run "todo init"',
            fg = typer.colors.RED
        )
        raise typer.Exit(1)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version", 
        "-v",
        help = "Show the application's version and exit.",
        callback = _version_callback,
        is_eager = True,
    )
) -> None:
    return

@app.command()
def add(
    name: str = typer.Argument(...),
    priority: int = typer.Option(2, "--priority", "-p", min=1, max=3),
    note: str = typer.Option("...", "--note", "-n"),
    due_date: str = typer.Option("", "--due-date", "-d"),
    steps: list[str] = typer.Option([], "--steps", "-s"),
    # steps: list[str] = typer.Argument(..., "--step", "-s"),
    tags: list[str] =  typer.Option([], "--tag", "-t"),
) -> None:
    todoer = get_todoer()
    task = Task(
        name,
        priority=Priority(priority),
        due_date=due_date,
        note=note,
        steps=steps,
        tags=tags,
        )

    task, error = todoer.add(task)
    if error:
        typer.secho(
            f'Adding task filed with "{ERRORS[error]}"',
            fg = typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""task "{task.name}" was added """
            f"""with priority: {task.priority.name}""",
            fg = typer.colors.GREEN,
        )

    

@app.command(name="list")
def list_all() -> None:
    todoer = get_todoer()
    todo_list = todoer.get_todo_list()
    if len(todo_list) == 0:
        typer.secho(
            "There are no tasks in the todo list yet", fg=typer.colors.RED
        )
        raise typer.Exit()
    typer.secho(
        "\ntodo list:\n", fg=typer.colors.BLUE, bold=True,
    )
    columns = (
        "ID.  ",
        "| Priority  ",
        "| Done  ",
        "| Description  ",
    )
    headers = "".join(columns)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho("-"*len(headers), fg=typer.colors.BLUE)
    for id, todo in enumerate(todo_list, 1):
        describe, priority, done = todo.values()
        typer.secho(
            f"{id}{(len(columns[0]) - len(str(id))) * ' '}"
            f"| ({priority}){(len(columns[1]) - len(str(priority)) - 4)* ' '}"
            f"| {done}{(len(columns[2]) - len(str(done)) - 2) * ' '}"
            f"| {describe}",
            fg=typer.colors.BLUE,
        )
    typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE)


@app.command(name="complete")
def set_done(todo_id: int = typer.Argument(...)) -> None:
    todoer = get_todoer()
    todo, error = todoer.set_done(todo_id)
    if error:
        typer.secho(
            f'Completing to-do # "{todo_id}" failed with "{ERRORS[error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""to-do # {todo_id} "{todo['Description']}" completed!""",
            fg=typer.colors.GREEN,
        )

@app.command()
def remove(
    todo_id: int = typer.Argument(...),
    force: bool = typer.Option(
        False,
        "--forece",
        "-f",
        help="Force deletion without confirmation.",
    ),
) -> None:
    todoer = get_todoer()

    def _remove():
        todo, error = todoer.remove(todo_id)
        if error:
            typer.secho(
                f'Removing todo # {todo_id} failed with "{ERRORS[error]}"',
                fg = typer.colors.RED,
            )
            raise typer.Exit(1)
        else:
            typer.secho(
                f"""to-do # {todo_id}: '{todo["Description"]}' was removed""",
                fg=typer.colors.GREEN,
            )
    
    if force:
        _remove()
    else:
        todo_list = todoer.get_todo_list()
        try:
            todo = todo_list[todo_id - 1]
        except IndexError:
            typer.secho("Invalid TODO_ID", fg=typer.colors.RED)
            raise typer.Exit(1)
        delete = typer.confirm(
            f"Delete todo # {todo_id}: {todo['Description']}?"
        )

        if delete:
            _remove()
        else:
            typer.echo("Operation canceled")

@app.command(name="clear")
def remove_all(
    force: bool = typer.Option(
        ...,
        prompt="Delete all todos?",
        help="Force deletion without confirmation."
    )
) -> None:
    todoer = get_todoer()
    if force:
        error = todoer.remove_all().error
        if error:
            typer.secho(
                f'Removing to-dos failed with "{ERRORS[error]}"',
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
        else:
            typer.secho("All todos were removed", fg = typer.colors.GREEN)
    else:
        typer.secho("Operation canceled")