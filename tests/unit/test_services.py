import pytest
from datetime import date, timedelta
from allocation import domain_model, services
from allocation.repository import Repository


@pytest.fixture
def repository():
    return Repository(products=[])


def test_returns_allocation(repository):
    services.add_batch(
        reference="b1", sku="LAMP", quantity=100, eta=None, repository=repository
    )
    result = services.allocate(
        orderid="o1", sku="LAMP", quantity=10, repository=repository
    )
    assert "b1" == result


def test_error_for_invalid_sku(repository):
    services.add_batch(
        reference="b1", sku="LAMP", quantity=100, eta=None, repository=repository
    )
    with pytest.raises(domain_model.InvalidSkuException):
        services.allocate(orderid="o1", sku="NOT", quantity=10, repository=repository)


def test_error_for_out_of_stock_exception(repository):
    services.add_batch(
        reference="b1", sku="LAMP", quantity=100, eta=None, repository=repository
    )
    with pytest.raises(domain_model.OutOfStockException):
        services.allocate(orderid="o1", sku="LAMP", quantity=200, repository=repository)


@pytest.fixture(params=[2, 10])
def qty(request):
    return request.param


def test_allocating_to_a_batch_if_available_greater_than_required_and_reduces_qty(
    qty, repository
):
    services.add_batch(
        reference="batch1", quantity=10, sku="aproduct", eta=None, repository=repository
    )
    product = repository.get("aproduct")
    assert 10 == product.batches[0].available_quantity
    services.allocate(
        orderid="order1", quantity=qty, sku="aproduct", repository=repository
    )
    assert 10 - qty == product.batches[0].available_quantity


def test_allocating_an_order_line_twice_does_nothing(repository):
    services.add_batch(
        reference="batch1", quantity=10, sku="somesku", eta=None, repository=repository
    )
    product = repository.get("somesku")
    assert 10 == product.batches[0].available_quantity
    services.allocate(
        orderid="order1", quantity=2, sku="somesku", repository=repository
    )
    assert 8 == product.batches[0].available_quantity
    services.allocate(
        orderid="order1", quantity=2, sku="somesku", repository=repository
    )
    assert 8 == product.batches[0].available_quantity


today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_prefers_warehouse_batches_to_shipments(repository):
    services.add_batch(
        reference="batch1", quantity=10, sku="somesku", eta=None, repository=repository
    )
    services.add_batch(
        reference="batch2", quantity=10, sku="somesku", eta=later, repository=repository
    )
    b = services.allocate(
        orderid="order1", quantity=2, sku="somesku", repository=repository
    )
    batch = repository.get("somesku").batches[0]
    assert b == batch.reference
    assert 8 == batch.available_quantity


def test_prefers_earlier_batches(repository):
    services.add_batch(
        reference="batch1", quantity=10, sku="somesku", eta=later, repository=repository
    )
    services.add_batch(
        reference="batch2", quantity=10, sku="somesku", eta=today, repository=repository
    )
    services.add_batch(
        reference="batch3",
        quantity=10,
        sku="somesku",
        eta=tomorrow,
        repository=repository,
    )
    b = services.allocate(
        orderid="order1", quantity=2, sku="somesku", repository=repository
    )

    assert "batch2" == b
    batch = next(
        b for b in repository.get("somesku").batches if b.reference == "batch2"
    )
    assert 8 == batch.available_quantity


def test_add_batch(repository):
    services.add_batch(
        reference="b1", sku="GREATLAMP", quantity=100, eta=None, repository=repository
    )
    assert repository.get("GREATLAMP").batches[0] is not None
