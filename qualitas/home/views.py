import logging

from flask import (Blueprint,
                   render_template,
                   request,
                   redirect,
                   url_for, flash)

from qualitas.lib.github_export import export
from qualitas.utils import render_csv

logging.basicConfig(level=logging.INFO)
LOGS = logging.getLogger(__name__)

home = Blueprint('home',
                 __name__,
                 template_folder='../templates/home')


@home.route('/', methods=['GET'])
def index():
    return render_template('home.html')
