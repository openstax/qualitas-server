def test_get_cnx_repos_view(test_client):
    response = test_client.get("/dashboards/cnx-repos")
    assert "<title>Qualitas | CNX Repos Dashboard</title>" in response


def test_get_url_commands_view(test_client):
    response = test_client.get("/dashboards/urlcommands")
    assert "<title>Qualitas | URL Commands Dashboard</title>" in response
