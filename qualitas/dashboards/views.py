from flask import (Blueprint,
                   current_app as app,
                   render_template)

from qualitas.admin.data import TUTOR_REPOS
from qualitas.dashboards.logic import get_repository_dashboard_data

dashboards = Blueprint('dashboards',
                       __name__,
                       url_prefix='/dashboards',
                       template_folder='../templates/dashboards')


@dashboards.route('/cnx-repos', methods=['GET'])
def cnx_repos():
    return render_template('cnx_repos.html')


@dashboards.route('/urlcommands', methods=['GET'])
def urlcommands():
    return render_template('urlcommands.html')


@dashboards.route('/cnx-json-loader', methods=['GET'])
def cnx_json_loader():
    return render_template('cnx_json_loader.html')


@dashboards.route('/tutor-repos')
def tutor_repos():
    client = app.github.client
    repository_data = get_repository_dashboard_data(client, TUTOR_REPOS)

    return render_template('tutor_repos.html', repositories=repository_data)


@dashboards.route('/cnx-repos-proto')
def cnx_repos_proto():
    from .proto_data import quick_links, cnx_server_files

    return render_template('cnx_repos.proto.html',
                           quick_links=quick_links,
                           cnx_server_files=cnx_server_files)
