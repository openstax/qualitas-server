def test_get_merge_pr_view_has_title(test_client):
    response = test_client.get("/tools/pr-export")
    assert "<title>Qualitas | PR Commit Exporter</title>" in response


def test_get_history_view_has_title(test_client):
    response = test_client.get("/tools/history-diff")
    assert "<title>Qualitas | Server Diff Tool</title>" in response
