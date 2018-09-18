import logging

from flask import current_app as app
from github3 import exceptions

from .client import GitHubClient

LOGS = logging.getLogger(__name__)


def get_pr_commit_data(repo_name, base, head):
    client = GitHubClient(app.config['GITHUB_USER'],
                          app.config['GITHUB_PASSWORD'])
    try:
        pr_commits = client.find_pr_commits(repo_name, base, head)
    except exceptions.NotFoundError:
        return None

    row_data = []
    if pr_commits:
        for commit in pr_commits:
            LOGS.info(commit)
            row = dict()
            row['repository'] = commit.repository
            row['commit_message'] = commit.message
            row['commit_sha'] = commit.sha
            row['commit_link'] = commit.html_url
            row['cl_trimmed'] = commit.short_html_url
            row['pr_id'] = commit.pr_id
            row['pr_link'] = commit.pr_link
            row['text'] = commit.text
            row_data.append(row)
        return row_data
    else:
        return None


