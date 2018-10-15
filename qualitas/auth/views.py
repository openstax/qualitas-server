import logging
from urllib.parse import quote, urlencode, parse_qs

import requests
from flask import (Blueprint,
                   render_template, current_app, redirect, url_for, request, session)
from flask_login import current_user
from flask_security import utils
from qualitas.auth.models import User
from qualitas.utils import redirect_next

from .forms import LoginForm
from ..core import db

auth = Blueprint('auth',
                 __name__,
                 url_prefix='/auth',
                 template_folder='../templates/auth')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_app.debug and current_app.config['GITHUB_AUTH']:
        form = LoginForm(request.form)

        if form.validate_on_submit():

            utils.login_user(form.user, False)
            db.session.merge(form.user)
            db.session.commit()
            return redirect(url_for('home.index'))

        return render_template('login.html', form=form)

    next = quote(quote(request.args['next'])) if 'next' in request.args else None
    qs = urlencode({
        'client_id': current_app.config['GITHUB_CLIENT_ID'],
        'redirect_uri': url_for('auth.authorized', next=next, _external=True)
    })
    url = 'https://github.com/login/oauth/authorize?{}'.format(qs)

    return redirect(url)


@auth.route('/login/authorized')
def authorized():
    next = quote(quote(request.args['next'])) if 'next' in request.args else None
    r = requests.post('https://github.com/login/oauth/access_token', {
        'client_id': current_app.config['GITHUB_CLIENT_ID'],
        'client_secret': current_app.config['GITHUB_CLIENT_SECRET'],
        'code': request.args['code'],
        'redirect_uri': url_for('auth.authorized', next=next, _external=True)
    })

    session['oauth_token'] = parse_qs(r.text)['access_token'][0]
    utils.login_user(User.oauth_load(token=session['oauth_token']))

    return redirect_next()


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    utils.logout_user()
    return redirect(url_for('home.index'))
