def test_products(client):
    response = client.get("/products")
    assert response.status_code == 200
    assert "products" in response.json
    assert 2 == len(response.json["products"])
    assert "Product 1" in [d["sku"] for d in response.json["products"]]
    assert "Product 2" in [d["sku"] for d in response.json["products"]]
