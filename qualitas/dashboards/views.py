from flask import (Blueprint,
                   render_template)

dashboards = Blueprint('dashboards',
                       __name__,
                       url_prefix='/dashboards',
                       template_folder='../templates/dashboards')


@dashboards.route('/cnx-repos', methods=['GET'])
def cnx_repos():
    return render_template('cnx_repos.html')


@dashboards.route('/cnx-repos-proto')
def cnx_repos_proto():
    from .proto_data import quick_links, cnx_server_files

    return render_template('cnx_repos.proto.html',
                           quick_links=quick_links,
                           cnx_server_files=cnx_server_files)
