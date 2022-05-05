import sqlite3
import pytest
from allocation import domain_model
from allocation.repository import ProductNotFoundException
from allocation.unit_of_work import SQLiteUnitOfWork, sqlite_connection


@pytest.fixture
def sqlite_uow():
    uow = SQLiteUnitOfWork(connection_factory=sqlite_connection("tests.db"))
    with uow:
        yield uow
    conn = sqlite_connection("tests.db")()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ALLOCATIONS")
    cursor.execute("DELETE FROM BATCHES")
    conn.commit()
    conn.close()


def test_save_product(sqlite_uow):
    product = domain_model.Product(
        sku="TABLE",
        batches=[domain_model.Batch(reference="batch_re_1", quantity=10, sku="TABLE")],
    )
    product.allocate(domain_model.OrderLine("order1", "TABLE", 2))
    product.allocate(domain_model.OrderLine("order2", "TABLE", 3))

    sqlite_uow.products.save(product)
    sqlite_uow.commit()

    sql_con = sqlite3.connect("tests.db")
    cursor = sql_con.cursor()
    cursor.execute("SELECT * FROM batches WHERE reference='batch_re_1'")
    res = cursor.fetchone()
    assert "batch_re_1" == res[0]
    assert "TABLE" == res[1]
    assert 10 == res[2]
    assert res[3] == ""

    cursor.execute("SELECT * FROM allocations WHERE reference='batch_re_1'")
    res = cursor.fetchall()
    assert 2 == len(res)
    assert "order2" in [r[0] for r in res]
    assert "order1" in [r[0] for r in res]
    assert "batch_re_1" == res[0][1]
    assert "batch_re_1" == res[1][1]
    assert 3 in [r[2] for r in res]
    assert 2 in [r[2] for r in res]

    sql_con.close()


def test_get_product(sqlite_uow):
    product = domain_model.Product(
        sku="TABLE",
        batches=[domain_model.Batch(reference="batch_re_1", quantity=10, sku="TABLE")],
    )
    product.allocate(domain_model.OrderLine("order1", "TABLE", 2))
    product.allocate(domain_model.OrderLine("order2", "TABLE", 3))

    sqlite_uow.products.save(product)
    product_saved = sqlite_uow.products.get(sku="TABLE")

    assert len(product_saved.batches) == len(product.batches)
    for b in product_saved.batches:
        batch = next(ba for ba in product.batches if b.reference == ba.reference)
        assert b._allocated == batch._allocated


def test_get_product_raise_exception_if_product_not_found(sqlite_uow):

    with pytest.raises(ProductNotFoundException):
        sqlite_uow.products.get(sku="NOTFOUND")


def test_add_product(sqlite_uow):
    product = domain_model.Product(
        sku="TABLE",
        batches=[domain_model.Batch(reference="batch_re_1", quantity=10, sku="TABLE")],
    )
    product.allocate(domain_model.OrderLine("order1", "TABLE", 2))
    product.allocate(domain_model.OrderLine("order2", "TABLE", 3))

    sqlite_uow.products.add(product)
    sqlite_uow.commit()

    sql_con = sqlite3.connect("tests.db")
    cursor = sql_con.cursor()
    cursor.execute("SELECT * FROM batches WHERE reference='batch_re_1'")
    res = cursor.fetchone()
    assert "batch_re_1" == res[0]
    assert "TABLE" == res[1]
    assert 10 == res[2]
    assert res[3] == ""

    cursor.execute("SELECT * FROM allocations WHERE reference='batch_re_1'")
    res = cursor.fetchall()
    assert 2 == len(res)
    assert "order2" in [r[0] for r in res]
    assert "order1" in [r[0] for r in res]
    assert "batch_re_1" == res[0][1]
    assert "batch_re_1" == res[1][1]
    assert 3 in [r[2] for r in res]
    assert 2 in [r[2] for r in res]

    sql_con.rollback()
    sql_con.close()


def test_list(sqlite_uow):
    product = domain_model.Product(
        sku="TABLE",
        batches=[domain_model.Batch(reference="batch_re_1", quantity=10, sku="TABLE")],
    )
    product.allocate(domain_model.OrderLine("order1", "TABLE", 2))
    product.allocate(domain_model.OrderLine("order2", "TABLE", 3))

    product_2 = domain_model.Product(
        sku="CHAIR",
        batches=[
            domain_model.Batch(reference="batch_chair_1", quantity=20, sku="CHAIR"),
            domain_model.Batch(reference="batch_chair_2", quantity=30, sku="CHAIR"),
        ],
    )
    product_2.allocate(domain_model.OrderLine("order232", "CHAIR", 4))
    product_2.allocate(domain_model.OrderLine("order233", "CHAIR", 8))

    sqlite_uow.products.add(product)
    sqlite_uow.products.add(product_2)

    products = sqlite_uow.products.list()

    assert len(products) == 2
    skus = [p.sku for p in products]
    assert "TABLE" in skus
    assert "CHAIR" in skus

    table = next(p for p in products if p.sku == "TABLE")
    assert 1 == len(table.batches)
    assert table.purchased_quantity == 10
    assert table.available_quantity == 5

    chair = next(p for p in products if p.sku == "CHAIR")
    assert 2 == len(chair.batches)
    assert chair.purchased_quantity == 50
    assert chair.available_quantity == 38


def test_list_returns_empty_list_if_no_products(sqlite_uow):
    assert [] == sqlite_uow.products.list()
