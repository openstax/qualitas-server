from qualitas.ext.flask_github import GitHubV4


def test_github_v4_call_api():
    gh = GitHubV4()
    result = gh.call_api("""\
query {
    organization(login: "openstax") {
        login
    }
}""")

    assert result == {
        'data': {
            'organization': {
                'login': 'openstax',
            }
        }
    }
