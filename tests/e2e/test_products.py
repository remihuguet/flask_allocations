def test_products(client):
    response = client.post(
        "/products/add_batch",
        json={
            "reference": "batch1333",
            "sku": "Product 1",
            "quantity": 10,
            "eta": None,
        },
    )
    response = client.post(
        "/products/add_batch",
        json={
            "reference": "batch222",
            "sku": "Product 2",
            "quantity": 10,
            "eta": None,
        },
    )

    response = client.get("/products")
    assert response.status_code == 200
    assert "products" in response.json
    assert 2 == len(response.json["products"])
    assert "Product 1" in [d["sku"] for d in response.json["products"]]
    assert "Product 2" in [d["sku"] for d in response.json["products"]]


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
