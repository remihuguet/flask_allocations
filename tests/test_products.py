def test_products(client):
    response = client.get("/products")
    assert response.status_code == 200
    assert "products" in response.json
    assert 2 == len(response.json["products"])
    assert "Product 1" == response.json["products"][0]["sku"]
