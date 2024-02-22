import sqlite3

import click
from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    # current_app.open_resource opens a file relative to the app package
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    """Clear the exisiting data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


# Need to register close_db and init_db_command functions to flask app
# To do that, we create a fucntion that takes the app object, and call that function from the __init__.py file.
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
