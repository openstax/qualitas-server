import json
import logging
import re
import urllib.error
from urllib.request import urlopen

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


def get_org_releases(github_v4_client, org):
    github_query = """\
query {
    organization(login: "%(org)s") {
        repositories(first: 100
                     orderBy: {
                         direction: DESC
                         field: PUSHED_AT
                     }
                     %(after)s) {
            nodes {
                name
                url
                pushedAt
                refs(refPrefix: "refs/tags/"
                     orderBy: {
                         direction: ASC
                         field: TAG_COMMIT_DATE
                     }
                     last: 1) {
                    nodes {
                        name
                        target { commitUrl }
                    }
                }
                defaultBranchRef {
                    target {
                        oid
                        commitUrl
                    }
                }
            }
            pageInfo {
                endCursor
                hasNextPage
            }
        }
    }
}
"""
    after = ''
    while True:
        result = github_v4_client.call_api(
            github_query % {'org': org, 'after': after}
        )['data']['organization']['repositories']

        for repo in result['nodes']:
            release = repo['refs']['nodes']
            head = repo['defaultBranchRef']
            if release:
                yield {
                    'name': repo['name'],
                    'url': repo['url'],
                    'pushed_at': repo['pushedAt'],
                    'release': {
                        'version': release[0]['name'],
                        'url': release[0]['target']['commitUrl'],
                    },
                    'head_ref': {
                        'commit': head['target']['oid'],
                        'url': head['target']['commitUrl'],
                    },
                }
        after = 'after: "{}"'.format(result['pageInfo']['endCursor'])
        if not result['pageInfo']['hasNextPage']:
            break


def parse_history_txt(server):
    content = urlopen('https://{}/history.txt'.format(server)).read().decode(
        'utf-8')
    latest = re.split('---+\n', re.split('===+\n', content, maxsplit=1)[0])
    release = {package: [version]
               for package, version in json.loads(latest[0]).items()}
    release_date = release.pop('date')[0]

    if 'webview' in release and '(' in release['webview'][0]:
        # webview version looks like:
        #    fc509073b895ac03bc66a3191204c1f44c648175 (v0.50.0-11-gfc50907)
        # only display the version in parentheses for webview
        version = release['webview'][0].split('(')[1].split(')')[0]
        release['webview'][0] = version

    for line in latest[1].splitlines():
        if '==' in line and not line.strip().startswith('#'):
            package_name, version = line.split('==')
        elif 'git+https' in line:
            package_name = line.split('/')[-1].split('@')[0].replace(
                '.git', '')
            version = line.split('@')[-1].split('#')[0]
        else:
            continue
        versions = release.setdefault(package_name, [])
        if version not in versions:
            versions.append(version)

    for package_name, versions in release.items():
        for i, version in enumerate(versions):
            commit = ''
            if '-g' in version:
                commit = version.rsplit('-g')[-1]
            elif re.match('[0-9a-f]{40}$', version):
                commit = version
                # truncate full commit hashes
                version = version[:7]
            versions[i] = {
                'version': version,
                'commit': commit,
            }

    return release_date, release


def get_pypi_release(package_name):
    known_wrong_matches = ('webview',)
    if package_name in known_wrong_matches:
        return None
    url = 'https://pypi.org/pypi/{}/json'.format(package_name)
    try:
        content = json.loads(urlopen(url).read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        LOGS.exception('pypi.org returns unexpected error')
        return None
    return {
        'version': content['info']['version'],
        'url': content['info']['release_url'],
    }
