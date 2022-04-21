def test_list_products(client):
    response = client.get("/admin/products")
    assert response.status_code == 200
    assert "<h2>Products list</h2>" in response.text
