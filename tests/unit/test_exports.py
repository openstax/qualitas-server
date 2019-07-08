from unittest import mock

from qualitas.exports.export import get_org_releases

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
