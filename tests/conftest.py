import pytest
from allocation import create_app
from allocation.unit_of_work import InMemoryUnitOfWork


@pytest.fixture
def uow():
    return InMemoryUnitOfWork()


@pytest.fixture
def client():
    app = create_app("InMemoryRepository")
    return app.test_client()
