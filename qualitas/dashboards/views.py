from flask import (Blueprint,
                   render_template)


dashboards = Blueprint('dashboards',
                       __name__,
                       url_prefix='/dashboards',
                       template_folder='../templates/dashboards')


@dashboards.route('/cnx-repos', methods=['GET'])
def cnx_repos():
    return render_template('cnx_repos.html')
