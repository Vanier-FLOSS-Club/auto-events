import json
from datetime import datetime, timezone
from typing import List, Optional


class Label:
    def __init__(self, data: dict):
        self.id: int = data.get("id", 0)
        self.name: str = data.get("name", "")
        self.description: str = data.get("description", "")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


class Issue:
    def __init__(self, data: dict):
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

    def closed_at(self) -> Optional[datetime]:
        # Returns the closed_at date as a UTC datetime object, or None if not closed。
        if self.closed_at_raw:
            try:
                return datetime.fromisoformat(self.closed_at_raw.replace("Z", "+00:00")).astimezone(timezone.utc)
            except ValueError:
                pass
        return None

    def to_dict(self):
        body = self.body

        start = "<!-- START -->"
        end = "<!-- END -->"
        json_start = "```json"
        json_end = "```"

        start_index = body.find(start)
        end_index = body.find(end)

        if start_index != -1 and end_index != -1:
            json_start_index = body.find(json_start)
            json_end_index = body.find(json_end, json_start_index + len(json_start))

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

        return {}
