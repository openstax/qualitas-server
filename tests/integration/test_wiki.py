def test_get_wiki_index_title(test_client):
    response = test_client.get("/wiki/")
    assert "<title>Qualitas | Wiki Pages</title>" in response
