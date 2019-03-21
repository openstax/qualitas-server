from .client import GitHubClient


class FlaskGitHub(object):

    _client_class = GitHubClient

    def __init__(self, app=None):
        self.client_id = None
        self.client_secret = None
        self.client = self._client_class()
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('GITHUB_CLIENT_ID', None)
        app.config.setdefault('GITHUB_CLIENT_SECRET', None)

        client_id = app.config['GITHUB_CLIENT_ID']






