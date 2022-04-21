def test_hello_world(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "<h2>Hello, World!</h2>" in response.data.decode("utf-8")
