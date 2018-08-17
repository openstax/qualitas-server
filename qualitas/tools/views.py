import logging

from flask import (Blueprint,
                   render_template,
                   request,
                   redirect,
                   url_for, flash)

from qualitas.tools.forms import PullRequestExportForm
from qualitas.lib.github_export import export
from qualitas.utils import render_csv

LOGS = logging.getLogger(__name__)

tools = Blueprint('tools',
                  __name__,
                  url_prefix='/tools',
                  template_folder='../templates/tools')


@tools.route('/pr-export', methods=['GET', 'POST'])
def pull_request_export():
    form = PullRequestExportForm(request.form)
    if form.validate_on_submit():
        LOGS.info('Pull Request Form validated correctly')
        repo_name = form.repo.data
        base = form.base.data
        head = form.head.data

        pr_commits = export.get_pr_commit_data(repo_name, base, head)

        if pr_commits:
            LOGS.info('There were pr {} commits found'.format(len(pr_commits)))
            fieldnames = pr_commits[0].keys()

            return render_csv(
                fieldnames, pr_commits, '{}-{}-{}'.format(repo_name.split('/')[1], base, head))
        else:
            LOGS.info('Something went wrong or no results were found')
            flash('There was a problem trying to find pull request commits. '
                  'Ensure you selected the proper repository')
            return redirect(url_for('tools.pull_request_export'))

    return render_template('pr_export.html', form=form)
