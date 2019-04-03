import logging
import time
from datetime import datetime
from urllib.parse import urlencode

import backoff
import requests

LOGS = logging.getLogger(__name__)


class ZenHubClient(object):
    def __init__(self, token, v4_token=None, session=requests.Session):
        self.public_api_url = 'https://api.zenhub.io/p1'
        self.v4_api_url = 'https://api.zenhub.io/v4'
        self.public_token = token
        self.v4_token = v4_token
        self.session = session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Authentication-Token': self.public_token,
        })

    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.Timeout, requests.exceptions.ConnectionError),
        max_tries=8
    )
    def request(self, method, url, **kwargs):
        LOGS.debug('%s %s with %s', method, url, kwargs)
        request_method = getattr(self.session, method)
        response = request_method(url, **kwargs)
        response.raise_for_status()
        self._deal_with_limits(response)

        return response.json()

    def post(self, url, **kwargs):
        """Sends a post request"""
        return self.request('post', url, **kwargs)

    def get(self, url, **kwargs):
        """Sends a get request"""
        return self.request('get', url, **kwargs)

    def _build_url(self, *args, **kwargs):
        """Builds the url to use the public api or v4 api url

        In order to use the v4 api the first keyword arg needs to be:

        `is_public=False`

        Example:

            self._build_url('repositories',
                             repo_id,
                            'connected',
                            is_public=False,
                            connected_issue_num=540)

        """
        is_public = True

        if 'is_public' in kwargs:
            is_public = kwargs.pop('is_public')

        if is_public:
            parts = [self.public_api_url]
        else:
            parts = [self.v4_api_url]

        parts.extend(args)
        parts = [str(p) for p in parts]

        if is_public:
            return '/'.join(parts)
        else:
            url = '/'.join(parts) + '?'
            qs = urlencode(kwargs)
            return url + qs

    def get_board(self, repo_id):
        url = self._build_url('repositories', repo_id, 'board', is_public=True)
        return self.get(url)

    def get_issue(self, repo_id, issue_number):
        url = self._build_url('repositories', repo_id, 'issues', issue_number, is_public=True)
        return self.get(url)

    def get_issue_events(self, repo_id, issue_number):
        url = self._build_url('repositories', repo_id, 'issues', issue_number, 'events',
                              is_public=True)
        return self.get(url)

    def get_connected_issue(self, repo_id, issue_number):
        url = self._build_url('repositories',
                              repo_id,
                              'connected',
                              is_public=False,
                              connected_issue_number=issue_number)
        return self.get(url)

    @staticmethod
    def _deal_with_limits(response):

        limit = used = wait_until = None

        if 'X-RateLimit-Limit' in response.headers:
            limit = int(response.headers['X-RateLimit-Limit'])

        if 'X-RateLimit-Used' in response.headers:
            used = int(response.headers['X-RateLimit-Used'])

        if 'X-RateLimit-Reset' in response.headers:
            wait_until = int(response.headers['X-RateLimit-Reset'])

        if wait_until:
            wait = (wait_until - datetime.now().timestamp())
            LOGS.info(
                f'Zenhub Request limit: {used} of {limit}, {wait} seconds to reset'
            )

        if limit and used:

            if limit - used <= 5:
                LOGS.warning(f'sleeping {wait} seconds')
                time.sleep(wait)
