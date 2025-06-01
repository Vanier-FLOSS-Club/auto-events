import json
from typing import List, Optional


class Label:
    def __init__(self, data: dict):
        """
        Initializes a Label object with the provided data.
        :param data: A dictionary containing label data
        """
        self.id: int = data.get("id", 0)
        self.name: str = data.get("name", "")
        self.description: str = data.get("description", "")

    def to_dict(self):
        """
        Converts the Label object to a dictionary representation.
        :return: A dictionary containing the label's id, name, and description
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


class Issue:
    def __init__(self, data: dict):
        """
        Initializes an Issue object with the provided data.
        :param data: A dictionary containing issue data
        """
        self.id: int = data.get("id", 0)
        self.url: str = data.get("url", "")
        self.number: int = data.get("number", 0)
        self.state: str = data.get("state", "")
        self.title: str = data.get("title", "")
        self.body: str = data.get("body", "")
        self.labels: List[Label] = [Label(label) for label in data.get("labels", [])]
        self.closed_at_raw: Optional[str] = data.get("closed_at")
        self.created_at_raw: str = data.get("created_at", "")
        self.updated_at_raw: str = data.get("updated_at", "")

    def to_dict(self):
        """
        Converts the Issue object directly to a JSON-compatible dictionary representation.
        :return: A dictionary containing the issue's JSON data.
        """
        body = self.body

        start = "<!-- START -->"
        end = "<!-- END -->"
        json_start = "```json"
        json_end = "```"

        # Find the start and end markers in the body
        start_index = body.find(start)
        end_index = body.find(end)

        # Check if both markers are found
        if start_index != -1 and end_index != -1:

            # If the markers are found, check for JSON markers
            json_start_index = body.find(json_start)
            json_end_index = body.find(json_end, json_start_index + len(json_start))

            # Extract the JSON part if both JSON markers are found
            if json_start_index != -1 and json_end_index != -1:
                body = body[json_start_index + len(json_start):json_end_index].strip()
                try:
                    return json.loads(body)
                except Exception as e:
                    print("Failed to compile JSON:", e)
                    return {}
            else:
                print("Missing JSON markers in the body.")
        else:
            print("Missing Start or End markers in the body.")

        # If no JSON part is found, return an empty dictionary
        return {}
