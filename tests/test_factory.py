from flaskr import create_app


def test_config():
    # Check that when we normally create an app, it's not in testing mode
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing


def test_hello(client):
    response = client.get("/hello")
    assert response.data == b"Hello, World!"
