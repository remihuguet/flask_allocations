import pytest
from allocation import app


@pytest.fixture
def client():
    return app.app.test_client()


def test_hello_world(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "<h1>Hello, World!</h1>" == response.data.decode("utf-8")
