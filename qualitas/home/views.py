import logging

from flask import (Blueprint,
                   render_template)


home = Blueprint('home',
                 __name__,
                 template_folder='../templates/home')


@home.route('/', methods=['GET'])
def index():
    return render_template('home.html')
