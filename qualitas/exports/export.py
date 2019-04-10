import logging

import github3

LOGS = logging.getLogger(__name__)


def get_pr_commit_data(github_client, zenhub_client, repo_name, base, head):
    try:
        pr_commits = github_client.find_pr_commits(repo_name, base, head)
    except github3.exceptions.NotFoundError:
        return None

    row_data = []
    if pr_commits:
        for commit in pr_commits:
            LOGS.info(commit)
            row = dict()
            row['repository'] = commit.repository.full_name
            row['repository_id'] = commit.repository.id
            row['base'] = base
            row['head'] = head
            row['commit_message'] = commit.message
            row['commit_sha'] = commit.sha
            row['commit_link'] = commit.html_url
            row['cl_trimmed'] = commit.short_html_url
            row['pr_id'] = commit.pr_id
            row['pr_link'] = commit.pr_link
            row['text'] = commit.text
            row['milestone'] = commit.milestone
            row['is_connected'] = check_issue_connection(zenhub_client,
                                                         commit.repository.id,
                                                         commit.pr_id)

            row_data.append(row)
        return row_data
    else:
        return None


def check_issue_connection(zenhub_client, repo_id, issue_id):
    events = zenhub_client.get_issue_events(repo_id, issue_id)

    for event in events:
        if event['type'] == 'disconnectPR':
            return False
        elif event['type'] == 'connectPR':
            return True
        else:
            continue

    return False
