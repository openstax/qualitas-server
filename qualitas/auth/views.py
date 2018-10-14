import logging

from flask import (Blueprint,
                   render_template, current_app, redirect, url_for, request)
from flask_security import utils

from .forms import LoginForm
from ..core import db

auth = Blueprint('auth',
                 __name__,
                 template_folder='../templates/auth')


@auth.route('/login', methods=['GET'])
def login():
    if current_app.debug and 'GITHUB_SECRET' not in current_app.config:
        form = LoginForm(request.form)

        if form.validate_on_submit():

            utils.login_user(form.user, False)
            db.session.commit()

            return redirect(url_for('home.index'))

        return render_template('login.html')
