import requests
from src.github_api_responses import Issue


def get_github_issues(owner, repo, token=None, label=None, state="all", per_page=100):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"

    headers = {
        "Accept": "application/vnd.github+json"
    }
    if token:
        headers["Authorization"] = f"token {token}"

    params = {
        "state": state,
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
        print("请求失败:", response.status_code, response.text)
        return []
