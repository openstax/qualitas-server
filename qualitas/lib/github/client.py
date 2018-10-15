import logging
import re

from github3 import GitHub
from github3.repos.commit import ShortCommit

LOGS = logging.getLogger(__name__)


class Commit(ShortCommit):
    """ Our model of a commit. github3 provides a nice abstraction.

    We've added a few things to help determine if something is a merge commit
    or squash commit. The latter is a bit more flaky because we have to check
    the commit message.

    For merge commits we check for parents > 1.

    For squash commits we look at the message for a particular regex match by
    looking for `(#PR_ID)` in the commit message.
    """
    class_name = 'Export Commit'

    def __init__(self, json, repo_name):
        self.repository = repo_name
        self._json_data = json
        self._update_attributes(json)

    def _update_attributes(self, commit):
        super(Commit, self)._update_attributes(commit)
        # Regular expression for extracting the PR ID from the message
        self._regex_pr_id = re.compile('((?<=\#)\d+|(?<=\(\#\))\d+)')
        # Regular expression for checking if a commit is a squash commit
        self._regex_squash = re.compile('\(\#\d+\)')
        self.short_html_url = self.html_url.replace(self.sha, self.sha[:7])
        self.short_sha = self.sha[:7]
        self.pr_link_template = 'https://github.com/{}/pull/{}'
        self.text_template = '{0} [PR {1}]({2})[{3}]({4})'

    @property
    def pr_id(self):
        if self.is_pr_commit:
            return re.search(self._regex_pr_id, self.message).group(0)
        else:
            LOGS.debug(f'PR ID not found{self.sha}')
            return None

    @property
    def is_pr_commit(self):
        return (self.is_merge_commit or self.is_squash_commit) and not self.is_master_merge

    @property
    def is_merge_commit(self):
        return len(self.parents) > 1

    @property
    def is_master_merge(self):
        return 'Merge' in self.message and 'branch' in self.message and 'master' in self.message

    @property
    def is_squash_commit(self):
        return bool(re.search(self._regex_squash, self.message))

    @property
    def pr_link(self):
        if self.is_pr_commit:
            return self.pr_link_template.format(self.repository, self.pr_id)
        else:
            return None

    @property
    def text(self):
        commit_msg = self.message

        if self.is_pr_commit:

            if '\n' in commit_msg:
                commit_msg = commit_msg.split('\n\n')[1][:50]

            _text = self.text_template.format(commit_msg,
                                              self.pr_id,
                                              self.short_html_url,
                                              self.short_sha,
                                              self.pr_link)

            return _text
        else:
            return None


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
