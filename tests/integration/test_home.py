def test_get_home_view(test_client):
    response = test_client.get("/")
    assert "<title>Qualitas | Home</title>" in response
