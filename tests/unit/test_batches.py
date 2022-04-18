from allocation.domain_model import Batch, OrderLine
from datetime import date, timedelta

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_allocating_an_order_line_to_a_batch_with_different_sku_dont_reduces_available_quantity():
    order_line = OrderLine(orderid="order1", quantity=2, sku="somesku")
    batch = Batch(reference="batch1", quantity=10, sku="othersku")
    assert 10 == batch.available_quantity
    batch.allocate(order_line)
    assert 10 == batch.available_quantity


def test_cannot_allocate_if_available_quantity_smaller_than_required():
    order_line = OrderLine(orderid="order1", quantity=6, sku="somesku")
    order_line_2 = OrderLine(orderid="order1", quantity=5, sku="somesku")
    batch = Batch(reference="batch1", quantity=10, sku="somesku")
    assert 10 == batch.available_quantity
    batch.allocate(order_line)
    assert 4 == batch.available_quantity
    batch.allocate(order_line_2)
    assert 4 == batch.available_quantity


def test_can_only_deallocate_allocated_lines():
    order_line = OrderLine(orderid="order1", quantity=2, sku="somesku")
    another_order_line = OrderLine(orderid="order1", quantity=56, sku="anothersku")
    batch = Batch(reference="batch1", quantity=10, sku="somesku")
    assert 10 == batch.available_quantity
    batch.deallocate(order_line)
    batch.allocate(order_line)
    assert 8 == batch.available_quantity
    batch.deallocate(another_order_line)
    assert 8 == batch.available_quantity
    batch.deallocate(order_line)
    assert 10 == batch.available_quantity
