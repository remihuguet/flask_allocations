import pytest
from allocation import app
from allocation.repository import Repository


@pytest.fixture
def repository():
    return Repository(products=[])


@pytest.fixture
def client():
    return app.test_client()
