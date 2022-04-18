def test_hello_world(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "<h1>Hello, World!</h1>" in response.data.decode("utf-8")
