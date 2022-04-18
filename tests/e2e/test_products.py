import pytest


def test_add_batch_endpoint_for_new_product(client):
    response = client.post(
        "/products/add_batch",
        json={"reference": "batch1", "sku": "somesku", "quantity": 10, "eta": None},
    )
    assert response.status_code == 201
    assert {"status": "OK"} == response.json

    products = client.get("/products").json["products"]
    assert "somesku" in [d["sku"] for d in products]


def test_add_batch_endpoint_returns_400_if_missing_parameter(client):
    response = client.post(
        "/products/add_batch",
        json={"reference": "batch1", "sku": "somesku", "eta": None},
    )
    assert response.status_code == 400
    response = client.post(
        "/products/add_batch",
        json={"reference": "batch1", "quantity": "str", "sku": "somesku", "eta": None},
    )
    assert response.status_code == 400


@pytest.fixture
def client_with_products(client):
    client.post(
        "/products/add_batch",
        json={
            "reference": "batch1333",
            "sku": "Product 1",
            "quantity": 10,
            "eta": None,
        },
    )
    client.post(
        "/products/add_batch",
        json={
            "reference": "batch222",
            "sku": "Product 2",
            "quantity": 10,
            "eta": None,
        },
    )
    yield client


def test_products(client_with_products):
    response = client_with_products.get("/products")
    assert response.status_code == 200
    assert "products" in response.json
    assert 3 == len(response.json["products"])
    assert set(["Product 1", "Product 2", "somesku"]) == set(
        d["sku"] for d in response.json["products"]
    )


def test_allocate_endpoint_returns_batchref(client_with_products):
    response = client_with_products.post(
        "/products/allocate",
        json={"orderid": "order1", "quantity": 2, "sku": "Product 2", "eta": None},
    )
    assert 201 == response.status_code
    assert "batchref" in response.json
    assert "batch222" == response.json["batchref"]


def test_allocate_endpoint_returns_400_if_missing_paramaters(client_with_products):
    response = client_with_products.post(
        "/products/allocate",
        json={"orderid": "order1", "quantity": "str", "sku": "Product 2", "eta": None},
    )
    assert 400 == response.status_code

    response = client_with_products.post(
        "/products/allocate",
        json={"quantity": 2, "sku": "Product 2", "eta": None},
    )
    assert 400 == response.status_code


def test_allocate_endpoint_returns_404_if_sku_invalid(client_with_products):
    response = client_with_products.post(
        "/products/allocate",
        json={"orderid": "order1", "quantity": 1, "sku": "Product 3", "eta": None},
    )
    assert 404 == response.status_code
    assert "Invalid sku" in response.json["error"]
