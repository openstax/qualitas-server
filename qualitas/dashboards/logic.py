from qualitas.core import github, githubv4
from qualitas.exports.export import (
    get_org_releases, parse_history_txt, get_cnx_deploy_versions,
)


def get_repository_dashboard_data(repositories):
    repos_data = []

    for repository in repositories:
        repo = get_github_repository_data(repository)

        repo_prepped = prepare_repo_data(repo)

        repos_data.append(repo_prepped)

    return repos_data


def prepare_repo_data(repo):
    repo_data = {}
    latest_tag = [tag for tag in repo.tags(number=1)]
    latest_commit = [commit for commit in repo.commits(number=1)]
    open_pull_requests = [pr for pr in repo.pull_requests()]

    repo_data["full_repo_name"] = repo.full_name
    repo_data["repo_name"] = repo.name
    repo_data["repo_url"] = repo.html_url
    repo_data["open_issues_count"] = repo.open_issues_count
    repo_data["issues_url"] = f"{repo.html_url}/issues"
    repo_data["latest_tag"] = latest_tag[0].name if latest_tag else ""
    repo_data["tags_url"] = f"{repo.html_url}/tags"
    repo_data["open_pull_requests_count"] = len(open_pull_requests)
    repo_data["pull_request_url"] = f"{repo.html_url}/pulls"
    repo_data["latest_commit_sha"] = latest_commit[0].sha
    repo_data["commit_url"] = f"{repo.html_url}/commits"

    return repo_data


def get_github_repository_data(repo_full_name):
    org_name = repo_full_name.split("/")[0]
    repo_name = repo_full_name.split("/")[1]
    repo = github.client.repository(org_name, repo_name)

    return repo


def version_unexpected(server_versions, repo):
    if not server_versions:
        # if the package is not installed on this server, nothing to do
        return False
    if len(server_versions) > 1:
        # more than one version of the same package, not ok
        return True

    # remove the sometimes prepended v in package versions
    version = server_versions[0]['version'].replace('v', '')
    commit = server_versions[0]['commit']
    tag_url = repo['latest_tag_url']
    head_commit = repo['head_full_commit']
    tag = repo['latest_tag'].replace('v', '')

    if commit and (commit in tag_url or commit == head_commit):
        # if commit is present and is the same as the latest tag or master,
        # it's ok
        return False
    if tag in version:
        # if version is "kitschy.kolache v0.76.0" and tag is "v0.76.0", it's ok
        return False

    # everything else is not ok
    return True


def get_cnx_dashboard_repos():
    org_repos = []
    for org in ('openstax', 'Rhaptos'):
        for r in get_org_releases(githubv4, org):
            org_repos.append(r)
    org_repos.sort(key=lambda r: r['pushed_at'], reverse=True)
    history_txt = {}
    release_dates = {}
    server_repos = set()
    for server in ('qa.cnx.org', 'staging.cnx.org', 'cnx.org'):
        release_dates[server], history_txt[server] = parse_history_txt(server)
        server_repos = server_repos.union(history_txt[server].keys())
    cnx_deploy_versions = get_cnx_deploy_versions()
    repos = []
    for r in org_repos:
        if r['name'] in server_repos:
            repo = {
                'name': r['name'],
                'url': r['url'],
                'latest_tag': r['release']['version'],
                'latest_tag_commit_url': r['release']['url'],
                'latest_tag_url': '{}/releases/tag/{}'.format(
                    r['url'], r['release']['version']),
                'head_commit': r['head_ref']['commit'][:7],
                'head_full_commit': r['head_ref']['commit'],
                'head_url': r['head_ref']['url'],
                'unexpected': [],
                'release_dates': {},
                'cnx_deploy_version': ', '.join(
                    cnx_deploy_versions.get(r['name'], [])),
            }
            for server_name, versions in history_txt.items():
                server_version = versions.get(r['name'], [])
                server_alias = server_name.split('.', 1)[0]
                repo[server_alias] = server_version
                if version_unexpected(server_version, repo):
                    repo['unexpected'].append(server_alias)
            repos.append(repo)
    return release_dates, repos
