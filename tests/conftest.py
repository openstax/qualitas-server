import pytest
from flask import Flask, Response

from qualitas.ext import flask_github


@pytest.fixture()
def app(request):
    app = Flask(__name__)
    app.response_class = Response
    app.debug = True
    app.config['SECRET_KEY'] = 'abigsecret'
    app.config['TESTING'] = True

    github = flask_github.FlaskGitHub()
    app.github = github.client
