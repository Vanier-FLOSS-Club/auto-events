import re
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

    def created_at(self) -> datetime:
        # Returns the created_at date as a UTC datetime object.
        return datetime.fromisoformat(self.created_at_raw.replace("Z", "+00:00")).astimezone(timezone.utc)

    def updated_at(self) -> datetime:
        # Returns the updated_at date as a UTC datetime object。
        return datetime.fromisoformat(self.updated_at_raw.replace("Z", "+00:00")).astimezone(timezone.utc)

    def get_due_date(self):
        # Get the due date from the body text, if available.
        match = re.search(r'Date:\s*(\d{4}-\d{2}-\d{2})', self.body)
        if match:
            return match.group(1)  # 返回字符串，也可以转成 datetime
        return None

    def to_dict(self):
        return {
            "name": self.title,
            "desc": self.body,
            "time": self.get_due_date(),
        }
