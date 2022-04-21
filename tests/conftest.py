import pytest
from allocation import create_app
from allocation.repository import InMemoryRepository


@pytest.fixture
def repository():
    return InMemoryRepository(products=[])


@pytest.fixture
def client():
    app = create_app("InMemoryRepository")
    return app.test_client()
