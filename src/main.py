import json
import os
import shutil

from src.request import get_github_issues

REPO_OWNER = "Vanier-FLOSS-Club"
REPO_NAME = "auto-events"

def format_link_data():
    return json.dumps(link_data, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    github_token = os.getenv("GITHUB_TOKEN", "")

    issues = get_github_issues(
        owner=REPO_OWNER,
        repo=REPO_NAME,
        token=github_token,
        label="event",
    )

    # Filter out issues that do not have the required JSON format in the body
    type_list = [issue.to_dict() for issue in issues]
    type_list = sorted(type_list, key=lambda x: x.get("time", ""))

    link_data = [
        {
            "type": "events",
            "typeName": "Upcoming: ",
            "typeDesc": "Conferences, Meetups, and Workshops",
            "typeList": type_list
        }
    ]

    output_path = r"output/eventData.json"

    if os.path.exists(os.path.dirname(output_path)):
        shutil.rmtree(os.path.dirname(output_path))
    os.makedirs(os.path.dirname(output_path))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(format_link_data())

    print(f"{len(issues)} Issue is saved to {output_path}")
