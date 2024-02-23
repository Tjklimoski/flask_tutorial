import sqlite3

import pytest
from flaskr.db import get_db


# Check that within the app context, get_db returns the same db every time
# Check that after the context, the db connection is closed
def test_get_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute("SELECT 1")

    assert "closed" in str(e.value)


# Check that init-db CLI command valls the init_db function and outputs msg
def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    # Monkeypatch is a built in fixture from pytest
    # monkeypatch replaces the init_db function with one that records that it's been called
    monkeypatch.setattr("flaskr.db.init_db", fake_init_db)
    result = runner.invoke(args=["init-db"])
    assert "Initialized" in result.output
    assert Recorder.called
