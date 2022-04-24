import sqlite3
import pytest
from allocation import domain_model
from allocation.repository import SQLiteRepository


@pytest.fixture
def sqlite_repo():
    yield SQLiteRepository("tests.db")


def test_save_product(sqlite_repo):
    product = domain_model.Product(
        sku="TABLE",
        batches=[domain_model.Batch(reference="batch_re_1", quantity=10, sku="TABLE")],
    )
    product.allocate(domain_model.OrderLine("order1", "TABLE", 2))
    product.allocate(domain_model.OrderLine("order2", "TABLE", 3))

    sqlite_repo.save(product)

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
    print(res)
    assert 2 == len(res)
    assert "order1" == res[0][0]
    assert "batch_re_1" == res[0][1]
    assert 2 == res[0][2]
    assert "order2" == res[1][0]
    assert "batch_re_1" == res[1][1]
    assert 3 == res[1][2]
