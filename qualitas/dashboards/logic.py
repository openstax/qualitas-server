def get_repository_dashboard_data(client, repositories):
    repos_version_data = []

    for repository in repositories:
        org_name = repository.split("/")[0]
        repo_name = repository.split("/")[1]
        repo_data = get_repository_data(client, org_name, repo_name)

        repos_version_data.append(repo_data)

    return repos_version_data


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
    repo_data["releases_url"] = f"{repo.html_url}/releases"
    repo_data["open_pull_requests_count"] = len(open_pull_requests)
    repo_data["pull_request_url"] = f"{repo.html_url}/pulls"
    repo_data["latest_commit_sha"] = latest_commit[0].sha
    repo_data["commit_url"] = f"{repo.html_url}/commits"

    return repo_data


def get_repository_data(client, org_name, repo_name):
    repo = client.repository(org_name, repo_name)

    repo_data = prepare_repo_data(repo)

    return repo_data



