from qualitas.ext.flask_zenhub.client import ZenHubClient


class ZenHub(object):
    """A Flask extension that adds ZenHub functionality to our core app."""

    def __init__(self, app=None, client_class=ZenHubClient):
        self.app = app
        self.client = client_class
        self.token = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.zenhub = self
        app.extensions['zenhub'] = self

        app.config.setdefault('ZENHUB_TOKEN')

        self.token = app.config['ZENHUB_TOKEN']

        self.client = self.init_client()

    def init_client(self):
        return self.client(token=self.token)
