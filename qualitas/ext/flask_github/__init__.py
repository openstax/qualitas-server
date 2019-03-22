import logging

from .client import GitHubClient

LOGS = logging.getLogger(__name__)


class FlaskGitHub(object):

    def __init__(self, app=None, client_class=GitHubClient):
        self.app = app
        self.client = client_class
        self.client_id = None
        self.client_secret = None
        self.client = None
        self.user = None
        self.password = None
        self.token = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        # Register with the application
        self.app = app
        app.github = self
        app.extensions['github'] = self

        # Configure the extension
        app.config.setdefault('GITHUB_USER', None)
        app.config.setdefault('GITHUB_PASSWORD', None)
        app.config.setdefault('GITHUB_CLIENT_ID', None)
        app.config.setdefault('GITHUB_CLIENT_SECRET', None)
        app.config.setdefault('GITHUB_AUTH_TOKEN', None)

        self.user = app.config['GITHUB_USER']
        self.password = app.config['GITHUB_PASSWORD']
        self.client_id = app.config['GITHUB_CLIENT_ID']
        self.client_secret = app.config['GITHUB_CLIENT_SECRET']
        self.token = app.config['GITHUB_AUTH_TOKEN']

        self.client = self.get_client()
        self.auto_login()

    def get_client(self):
        return GitHubClient()

    def token_login(self):
        LOGS.info("Authenticating GitHub client with token")
        self.client.login(token=self.token)

    def basic_login(self):
        LOGS.debug("Authenticating GitHub client with basic auth")
        if self.user and self.password:
            self.client.login(self.user, self.password)
        else:
            LOGS.warning("No GitHub username and password found for basic auth."
                         "Your requests may be limited if they exceed the limits.")

    def auto_login(self):
        if self.token:
            self.token_login()
        else:
            self.basic_login()
