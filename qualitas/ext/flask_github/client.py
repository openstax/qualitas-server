import logging

from github3 import GitHub

from .models import Commit

LOGS = logging.getLogger(__name__)


class GitHubClient(GitHub):
    """ github3.py Client wrapper

    This class wraps the github3 client and provides a public api for use in
    the framework.
    """

    def __init__(self, user=None, password=None, token=None):
        super(GitHubClient, self).__init__(user, password, token)

    def _compare_commits(self, repo_name, base, head):
        org_name = repo_name.split('/')[0]
        repo_name = repo_name.split('/')[1]

        repo = self.repository(org_name, repo_name)
        return repo.compare_commits(base, head)

    def find_pr_commits(self, repo_name, base, head):
        comparison = self._compare_commits(repo_name, base, head)
        _pr_commits = []

        for commit in comparison.commits:
            # Use our commit object
            commit = Commit(commit._json_data, repo_name)
            LOGS.info(f'Checking commit {commit.sha}')

            if commit.is_pr_commit:
                LOGS.info(commit)
                _pr_commits.append(commit)

        if _pr_commits:
            LOGS.info(f'{len(_pr_commits)} PR commits were returned')
            return _pr_commits
        else:
            return None