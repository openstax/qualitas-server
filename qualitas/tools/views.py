import logging
from urllib.parse import urljoin

import requests
from flask import (Blueprint,
                   render_template,
                   request,
                   redirect,
                   url_for,
                   flash)

from qualitas.core import github, zenhub
from qualitas.lib.parsers.release import ReleaseParser
from qualitas.tools.forms import PullRequestExportForm, ServerDiffForm
from qualitas.exports import export
from qualitas.utils import render_csv

LOGS = logging.getLogger(__name__)

tools = Blueprint('tools',
                  __name__,
                  template_folder='../templates/tools')


@tools.route('/pr-export', methods=['GET', 'POST'])
def pull_request_export():
    form = PullRequestExportForm()

    if request.method == 'POST':
        form_data = dict(request.form)

        view_data = form.data["view_data"] == "on"
        form_data.pop('csrf_token')
        form_data.pop('view_data')
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
            repo_name = form_data[f'repo_{n}']
            base = form_data[f'base_{n}']
            head = form_data[f'head_{n}']
            LOGS.info(f'Currently processing {repo_name} b{base} h{head}')
            commits = export.get_pr_commit_data(github.client,
                                                zenhub.client,
                                                repo_name,
                                                base,
                                                head)
            if commits:
                pr_commits.extend(commits)
            else:
                LOGS.info(f'No PR Commits found for {repo_name}')

        if pr_commits and not view_data:
            LOGS.info('There were pr {} commits found'.format(len(pr_commits)))
            fieldnames = pr_commits[0].keys()

            return render_csv(fieldnames, pr_commits, 'pr-commits')
        elif pr_commits and view_data:
            return render_template('pr_export_view.html',
                                   pr_commits=pr_commits)
        else:
            LOGS.warning('Something went wrong or no results were found')
            flash('There was a problem trying to find pull request commits. '
                  'Ensure you filled out all fields correctly')
            return redirect(url_for('tools.pull_request_export'))

    return render_template('pr_export.html', form=form)


@tools.route('/history-diff', methods=['GET', 'POST'])
def history_diff():
    releases_separator = '==============================='
    form = ServerDiffForm(request.form)
    diff = ""

    if form.validate_on_submit():
        server1 = form.server_1.data
        server2 = form.server_2.data

        server1_url = urljoin(server1, 'history.txt')
        server2_url = urljoin(server2, 'history.txt')

        # Set a boolean if the servers are the same. If they are the same then
        # We will return the diff of most current release and the previous release.
        # If they are different we will diff the current release of each.
        is_same = server1_url == server2_url

        if is_same:
            server1_text = requests.get(server1_url).text
            server1_releases = [ReleaseParser(i) for i in
                                server1_text.split(releases_separator)]

            current_release = server1_releases[0]
            previous_release = server1_releases[1]
            diff = current_release.diff(previous_release)
        else:
            server1_text = requests.get(server1_url).text
            server1_releases = [ReleaseParser(i) for i in
                                server1_text.split(releases_separator)]

            server2_text = requests.get(server2_url).text
            server2_releases = [ReleaseParser(i) for i in
                                server2_text.split(releases_separator)]

            server1_current_release = server1_releases[0]
            server2_current_release = server2_releases[0]

            diff = server1_current_release.diff(server2_current_release)

    return render_template('history_diff.html',
                           form=form,
                           diff=diff)
