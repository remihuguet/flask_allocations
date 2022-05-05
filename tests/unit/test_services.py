import pytest
from datetime import date, timedelta
from allocation import domain_model, services


def test_returns_allocation(uow):
    services.add_batch(reference="b1", sku="LAMP", quantity=100, eta=None, uow=uow)
    result = services.allocate(orderid="o1", sku="LAMP", quantity=10, uow=uow)
    assert "b1" == result


def test_error_for_invalid_sku(uow):
    services.add_batch(reference="b1", sku="LAMP", quantity=100, eta=None, uow=uow)
    with pytest.raises(domain_model.InvalidSkuException):
        services.allocate(orderid="o1", sku="NOT", quantity=10, uow=uow)


def test_error_for_out_of_stock_exception(uow):
    services.add_batch(reference="b1", sku="LAMP", quantity=100, eta=None, uow=uow)
    with pytest.raises(domain_model.OutOfStockException):
        services.allocate(orderid="o1", sku="LAMP", quantity=200, uow=uow)


@pytest.fixture(params=[2, 10])
def qty(request):
    return request.param


def test_allocating_to_a_batch_if_available_greater_than_required_and_reduces_qty(
    qty, uow
):
    services.add_batch(
        reference="batch1", quantity=10, sku="aproduct", eta=None, uow=uow
    )
    product = uow.products.get("aproduct")
    assert 10 == product.batches[0].available_quantity
    services.allocate(orderid="order1", quantity=qty, sku="aproduct", uow=uow)
    assert 10 - qty == product.batches[0].available_quantity


def test_allocating_an_order_line_twice_does_nothing(uow):
    services.add_batch(
        reference="batch1", quantity=10, sku="somesku", eta=None, uow=uow
    )
    product = uow.products.get("somesku")
    assert 10 == product.batches[0].available_quantity
    services.allocate(orderid="order1", quantity=2, sku="somesku", uow=uow)
    assert 8 == product.batches[0].available_quantity
    services.allocate(orderid="order1", quantity=2, sku="somesku", uow=uow)
    assert 8 == product.batches[0].available_quantity


today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_prefers_warehouse_batches_to_shipments(uow):
    services.add_batch(
        reference="batch1", quantity=10, sku="somesku", eta=None, uow=uow
    )
    services.add_batch(
        reference="batch2", quantity=10, sku="somesku", eta=later, uow=uow
    )
    b = services.allocate(orderid="order1", quantity=2, sku="somesku", uow=uow)
    batch = uow.products.get("somesku").batches[0]
    assert b == batch.reference
    assert 8 == batch.available_quantity


def test_prefers_earlier_batches(uow):
    services.add_batch(
        reference="batch1", quantity=10, sku="somesku", eta=later, uow=uow
    )
    services.add_batch(
        reference="batch2", quantity=10, sku="somesku", eta=today, uow=uow
    )
    services.add_batch(
        reference="batch3",
        quantity=10,
        sku="somesku",
        eta=tomorrow,
        uow=uow,
    )
    b = services.allocate(orderid="order1", quantity=2, sku="somesku", uow=uow)

    assert "batch2" == b
    batch = next(
        b for b in uow.products.get("somesku").batches if b.reference == "batch2"
    )
    assert 8 == batch.available_quantity


def test_add_batch(uow):
    services.add_batch(reference="b1", sku="GREATLAMP", quantity=100, eta=None, uow=uow)
    assert uow.products.get("GREATLAMP").batches[0] is not None
