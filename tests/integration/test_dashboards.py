import re
from unittest import mock

from ..helpers import data_loader


def test_get_old_cnx_repos_view(test_client):
    response = test_client.get("/dashboards/old-cnx-repos")
    assert "<title>Qualitas | CNX Repos Dashboard</title>" in response


def test_get_cnx_repos_view(test_client):
    p1 = mock.patch('qualitas.dashboards.logic.get_pypi_release')
    get_pypi_release = p1.start()
    get_pypi_release.side_effect = lambda package: \
        data_loader('integration/pypi-releases.json').get(package)

    p2 = mock.patch('qualitas.dashboards.logic.parse_history_txt')
    parse_history_txt = p2.start()
    parse_history_txt.side_effect = lambda server: \
        data_loader('integration/history-txt-{}.json'.format(server))

    p3 = mock.patch('qualitas.dashboards.logic.get_org_releases')
    get_org_releases = p3.start()
    get_org_releases.side_effect = lambda client, org: \
        data_loader('integration/org-releases-{}.json'.format(org))

    response = test_client.get("/dashboards/cnx-repos")

    # parse the table
    body = response.body.decode('utf-8')
    tbody = body.split('<tbody>')[1].split('</tbody>')[0]
    table_content = []
    for tr in tbody.split('</tr>')[:-1]:
        table_content.append([
            e for i, e in enumerate(re.split('\s*</?td[^>]*>\s*', tr))
            if i % 2 == 1])

    # check the first row of the table
    repo, master, tag, pypi, qa_version, staging_version, prod_version = \
        table_content[0]
    assert '"https://github.com/openstax/cnx-recipes"' in repo
    assert '8fea596 (v1.34.0)' in master
    assert 'v1.34.0' in tag
    assert 'https://pypi.org/project/cnx-recipes/1.34.0' in pypi
    assert 'github.com' in qa_version and '8fea596 (v1.34.0)' in qa_version
    assert staging_version == '1.34.0'
    assert prod_version == '1.33.0'


def test_get_url_commands_view(test_client):
    response = test_client.get("/dashboards/urlcommands")
    assert "<title>Qualitas | URL Commands Dashboard</title>" in response
