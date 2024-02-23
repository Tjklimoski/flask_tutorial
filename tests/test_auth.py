import pytest
from flask import g, session
from flaskr.db import get_db


# Check that when we make a get req to /auth/register we get back a web page
# Check that when we post to /auth/register the response redirects to /auth/login
# Check that
def test_register(client, app):
    assert client.get("/auth/register").status_code == 200
    response = client.post("/auth/register", data={"username": "a", "password": "a"})
    assert response.headers["location"] == "/auth/login"

    with app.app_context():
        assert (
            get_db()
            .execute(
                "SELECT * FROM user WHERE username = 'a'",
            )
            .fetchone()
            is not None
        )


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("", "", b"Username is required"),
        ("a", "", b"Password is required"),
        ("test", "test", b"already registered"),
    ),
)
def test_register_validate_input(client, username, password, message):
    response = client.post(
        "/auth/register", data={"username": username, "password": password}
    )
    assert message in response.data
