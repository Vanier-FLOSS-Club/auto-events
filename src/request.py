import requests

from src.github_api_responses import Issue


def get_github_issues(owner, repo, token=None, label=None, per_page=100):
    """
    Fetches issues from a GitHub repository.
    This function retrieves open issues from a specified GitHub repository,
    optionally filtered by a specific label.
    :param owner: The owner of the GitHub repository
    :param repo: The name of the GitHub repository
    :param token: GitHub personal access token for authentication (optional)
    :param label: The label to filter issues by (optional)
    :param per_page: The number of issues to retrieve per page (default is 100)
    :return: List of Issue objects representing the issues in the repository.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"

    headers = {
        "Accept": "application/vnd.github+json"
    }
    if token:
        headers["Authorization"] = f"token {token}"

    params = {
        "state": "open",
        "per_page": per_page,
    }
    if label:
        params["labels"] = label

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        raw_data = response.json()
        issues = [Issue(item) for item in raw_data if "pull_request" not in item]
        return issues
    else:
        print("Failed to Request:", response.status_code, response.text)
        return []
