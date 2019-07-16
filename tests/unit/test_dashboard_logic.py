from qualitas.dashboards.logic import version_unexpected


def test_version_unexpected():
    assert version_unexpected([], {}) is False
    assert version_unexpected([
        {'commit': '', 'version': '1.2'},
        {'commit': '', 'version': '1.3'}], {}) is True

    assert version_unexpected([
        {'commit': '8fea5960478aab5349edd375ba91f04c307a4066',
         'version': '8fea596'}
    ], {
        'latest_tag_url': 'https://github.com/openstax/cnx-recipes/'
        'commit/8fea5960478aab5349edd375ba91f04c307a4066',
        'head_full_commit': '8fea5960478aab5349edd375ba91f04c307a4066',
        'pypi': None,
        'latest_tag': 'v1.2.3',
    }) is False

    assert version_unexpected([
        {'commit': 'aeee572',
         'version': 'v2.42.6-26-gaeee572'},
    ], {
        'latest_tag_url': 'https://github.com/openstax/cnx-deploy/'
        'commit/4c13b9014ccca257711faf845397dd864db4bdf5',
        'head_full_commit': '4c13b9014ccca257711faf845397dd864db4bdf5',
        'pypi': None,
        'latest_tag': 'v2.43.0',
    }) is True

    assert version_unexpected([
        {'commit': '',
         'version': '0.144'},
    ], {
        'latest_tag_url': 'https://github.com/Rhaptos/Products.RhaptosPrint/'
        'commit/34afd2be4a064f0312fba5313430f6440f4ffede',
        'head_full_commit': '34afd2be4a064f0312fba5313430f6440f4ffede',
        'pypi': None,
        'latest_tag': '0.108',
    }) is True

    assert version_unexpected([
        {'commit': '',
         'version': 'kitschy.kolache v0.76.0'},
    ], {
        'latest_tag_url': 'https://github.com/openstax/oer.exports/'
        'commit/3bd2b75bce5660cb4344c79862351a1ecbda3272',
        'head_full_commit': '3bd2b75bce5660cb4344c79862351a1ecbda3272',
        'pypi': None,
        'latest_tag': 'v0.76.0',
    }) is False

    assert version_unexpected([
        {'commit': '',
         'version': '4.13.0'},
    ], {
        'latest_tag_url': 'https://github.com/openstax/cnx-archive/'
        'commit/7161a1a5bb79f506e02f21032bded114302e0517',
        'head_full_commit': '7161a1a5bb79f506e02f21032bded114302e0517',
        'pypi': {'version': '4.13.0'},
        'latest_tag': 'v4.13.0',
    }) is False
