import pytest
from allocation import app


@pytest.fixture
def client():
    return app.test_client()
