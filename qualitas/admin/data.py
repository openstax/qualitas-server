"""FIXME: These values are placeholders until we turn them into proper data
models and store them in the database. That is being planned for in the future
but right now this will get us by.
"""


def get_tutor_repos():
    return [
        'openstax/accounts',
        'openstax/exercises',
        'openstax/tutor-js',
        'openstax/biglearn-api',
        'openstax/biglearn-local-query',
        'openstax/biglearn-scheduler',
        'openstax/biglearn-sparfa-server',
        'openstax/biglearn-sparfa-algs',
        'openstax/openstax-cms',
        'openstax/os-webview',
        'openstax/oscms-deployment',
        'openstax/ospayments',
        'openstax/ospayments-deployment',
        'openstax/response-collector',
        'openstax/tutor-deployment',
        'openstax/tutor-server'
    ]


CNX_HOSTS = [
    'https://cnx.org',
    'https://qa.cnx.org',
    'https://staging.cnx.org',
    'https://devb.cnx.org',
    'https://content01.cnx.org'
]
