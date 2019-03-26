import logging

from .client import GitHubClient

LOGS = logging.getLogger(__name__)


class GitHub(object):
    """A Flask extension that adds GitHub functionality to our core app.

    Extensions are used by Flask to add functionality. This class essentially
    registers our GitHubClient to the core app so that it's accessible to any
    parts of the app that require it.

    The minimum requirement for a Flask extenison is that it has a `init_app`
    method that acts as a callback. The reason for this is so that it can be
    configured and registered with the core app in 2 ways.

    The first doesn't use an application factory:

    ```
    app = Flask(__name__)

    github = GitHub(app)
    ```

    The second uses an application factory:

    ```
    github = GitHub()

    def create_app():
        app = Flask(__name__)

        github = github.init_app(app)

        return app
    ```
    """

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
        """Returns our wrapper of the github3 GitHub client

        The main github3 client that we wrap doesn't require authentication so
        we go ahead and instantiate it so we have it available.
        """
        return GitHubClient()

    def token_login(self):
        LOGS.info("Authenticating GitHub client with token")
        self.client.login(token=self.token)

    def basic_login(self):
        LOGS.debug("Authenticating GitHub client with basic auth")
        if self.user and self.password:
            self.client.login(self.user, self.password)
        else:
            LOGS.warning("No GitHub username and password found for basic auth. "
                         "Your requests may be limited if they exceed the limits.")

    def auto_login(self):
        if self.token:
            self.token_login()
        else:
            self.basic_login()
