import logging

from flask import (Blueprint,
                   render_template,
                   request,
                   redirect,
                   url_for, flash)

from qualitas.tools.forms import PullRequestExportForm
from qualitas.lib.github_export import export
from qualitas.utils import render_csv

logging.basicConfig(level=logging.DEBUG)
LOGS = logging.getLogger(__name__)

tools = Blueprint('tools',
                  __name__,
                  url_prefix='/tools',
                  template_folder='../templates/tools')


@tools.route('/pr-export', methods=['GET', 'POST'])
def pull_request_export():
    form = PullRequestExportForm()

    if request.method == 'POST':
        form_data = dict(request.form)
        # Remove CSRF Token
        form_data.pop('csrf_token')
        LOGS.debug(form_data)

        # Ensure the number of fields is a multiple of 3
        if len(form_data) % 3 != 0:
            flash('Incorrect number of entries per repository')
            return redirect(url_for('tools.pull_request_export'))

        LOGS.info('The POSTED form has the correct number of fields')

        # Determine the number of repos
        repo_num = int(len(form_data) / 3)

        LOGS.info(f'Total Repos to check are {repo_num}')

        pr_commits = []

        for n in range(1, repo_num + 1):
            repo_name = form_data[f'repo_{n}'][0]
            base = form_data[f'base_{n}'][0]
            head = form_data[f'head_{n}'][0]
            LOGS.info(f'Currently processing {repo_name} b{base} h{head}')
            commits = export.get_pr_commit_data(repo_name,
                                                base,
                                                head)
            if commits:
                pr_commits.extend(commits)
            else:
                LOGS.info(f'No PR Commits found for {repo_name}')

        if pr_commits:
            LOGS.info('There were pr {} commits found'.format(len(pr_commits)))
            fieldnames = pr_commits[0].keys()

            return render_csv(
                fieldnames, pr_commits, 'pr-commits')
        else:
            LOGS.info('Something went wrong or no results were found')
            flash('There was a problem trying to find pull request commits. '
                  'Ensure you filled out all fields correctly')
            return redirect(url_for('tools.pull_request_export'))

    return render_template('pr_export.html', form=form)
