from qualitas.exports.export import get_pr_commit_data
from .helpers import data_loader


def test_get_pr_commit_data(test_client):

    # FIXME: This test is probably best handled with betamax so that we're not
    # having to make 3rd party requests on every test run. That's not often
    # ATM. Updates to qualitas are not very frequent right now.
    # As we advance the test framework we can make this better

    data = data_loader("pr_export.json")
    gh_client = test_client.app.github.client
    zh_client = test_client.app.zenhub.client

    repo = "openstax/biglearn-api"
    base = "ce2503b458a36053c5b7cb4fa88706a66e447fc2"
    head = "3c0fdb4ad15127d0d3eac2ff9ba376f94bf4c24f"

    pr_data = get_pr_commit_data(gh_client, zh_client, repo, base, head)

    assert data == pr_data
