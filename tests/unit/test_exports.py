import io
import json
from unittest import mock
from urllib.error import HTTPError

from qualitas.exports.export import (
    get_org_releases, parse_history_txt, get_cnx_deploy_versions
)

from ..helpers import data_loader


def test_get_org_releases():
    mock_gh_client = mock.Mock()

    def mock_call_api(*args, **kwargs):
        if mock_gh_client.call_api.call_count == 1:
            return data_loader('unit/latest-tags-1.json')
        else:
            return data_loader('unit/latest-tags-2.json')

    mock_gh_client.call_api.side_effect = mock_call_api
    assert list(get_org_releases(mock_gh_client, 'openstax')) == \
        data_loader('unit/latest-tags-export.json')


def test_parse_history_txt():
    with mock.patch('qualitas.exports.export.urlopen') as urlopen:
        urlopen.return_value = io.BytesIO(data_loader(
            'unit/cnx-history.txt').encode('utf-8'))
        release_date, versions = parse_history_txt('qa.cnx.org')
    assert release_date == '2019-07-01 08:46:05 CDT'
    # different versions for archive / publishing / press
    assert versions['cnx-db'] == [
        {'version': '3.2.0', 'commit': ''},
        {'version': '3.1.1', 'commit': ''},
    ]
    # non python version
    assert versions['webview'] == [{
        'version': 'v0.51.0', 'commit': ''}]
    assert versions['cnx-deploy'] == [{
        'version': 'v2.42.6', 'commit': ''}]
    # normal python package
    assert versions['cnx-archive'] == [{
        'version': '4.12.0', 'commit': ''}]
    # github tag only, python but not a package
    assert versions['press'] == [{
        'version': '8.1.0', 'commit': ''}]
    # github branch
    assert versions['cnx-query-grammar'] == [{
        'version': '8484d2c',
        'commit': '8484d2caed62aa5cdf1e0a631b1301a73cd5dbe8',
    }]
    # legacy
    assert versions['Products.RhaptosSite'] == [{
        'version': '1.49', 'commit': ''}]


def test_get_cnx_deploy_versions():
    with mock.patch('qualitas.exports.export.urlopen') as urlopen:
        urlopen.return_value = io.BytesIO(data_loader(
            'unit/cnx-deploy-master.zip', 'rb'))
        versions = get_cnx_deploy_versions()

    assert versions['Products.CMFSquidTool'] == {'1.5.1'}
    assert versions['lxml'] == {'3.3.6', '4.4.0'}
    assert versions['webview'] == {'v0.54.0'}
