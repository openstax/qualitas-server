from qualitas.core import github


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
