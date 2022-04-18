def test_list_products(client):
    response = client.get("/admin/products")
    assert response.status_code == 200
    assert "<h1>Products list</h1>" in response.text
