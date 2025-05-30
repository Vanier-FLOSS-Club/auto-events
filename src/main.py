import os
import re

from src.request import get_github_issues

# Repository information for the GitHub API.
REPO_OWNER = "Vanier-FLOSS-Club"
REPO_NAME = "auto-events"


def clean_desc(body: str) -> str:
    body = re.sub(r"(?i)^.*deadline:\s*\d{4}-\d{2}-\d{2}.*\n?", "", body, flags=re.MULTILINE).strip()
    body = body.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return body


def format_event(event):
    return f'''      {{
        name: "{event['name']}",
        desc: "{clean_desc(event['desc'])}",
        time: "{event['time']}"
      }}'''


def format_link_data():
    formatted = "// Upcoming events data\nconst linkData = [\n"
    for group in link_data:
        formatted += f'''  {{
    type: "{group['type']}",
    typeName: "{group['typeName']}",
    typeDesc: "{group['typeDesc']}",
    typeList: [
{",\n".join(format_event(e) for e in group['typeList'])}
    ]
  }}'''
    formatted += "\n];\n\nexport default linkData;\n"
    return formatted


if __name__ == "__main__":
    github_token = os.getenv("GITHUB_TOKEN", "")

    issues = get_github_issues(
        owner=REPO_OWNER,
        repo=REPO_NAME,
        token=github_token
    )

    type_list = [issue.to_dict() for issue in issues]

    link_data = [
        {
            "type": "events",
            "typeName": "Upcoming: ",
            "typeDesc": "Conferences, Meetups, and Workshops",
            "typeList": type_list
        }
    ]

    output_path = r"output/eventData.mjs"

    # Cleanup the output directory before writing
    if os.path.exists(os.path.dirname(output_path)):
        os.removedirs(os.path.dirname(output_path))
    os.makedirs(os.path.dirname(output_path))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(format_link_data())

    print(f"{len(issues)} Issue is saved to {output_path}")
