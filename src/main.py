import json
import os
import shutil
import json_to_js_converter

from src.request import get_github_issues

REPO_OWNER = "Vanier-FLOSS-Club"
REPO_NAME = "auto-events"

def format_link_data():
    """
    Formats the link data into a JSON string.
    :return: JSON string of the link data
    """
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
    # Sort the issues by the "time" field if it exists
    type_list = sorted(type_list, key=lambda x: x.get("time", ""))

    # Format the data into the required structure
    link_data = [
        {
            "type": "events",
            "typeName": "Upcoming: ",
            "typeDesc": "Conferences, Meetups, and Workshops",
            "typeList": type_list
        }
    ]

    # Print the number of issues saved
    print(f"{len(issues)} Issue(s) saved")

    # Convert to .mjs file
    js_code = json_to_js_converter.json_to_js_object(format_link_data())

    output_js_path = r"output/eventData.mjs"

    # Ensure the output directory
    if os.path.exists(os.path.dirname(output_js_path)):
        shutil.rmtree(os.path.dirname(output_js_path))
    os.makedirs(os.path.dirname(output_js_path))

    # Write the JavaScript code to the output file
    with open(output_js_path, "w", encoding="utf-8") as f:
        f.write(js_code)

    # Print the output path
    print(f"Saved to {output_js_path}")
