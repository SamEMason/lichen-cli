from pathlib import Path
from typing import Any


class Node:
    """Template file tree node"""

    def __init__(self, type: str, path: Path, template: Path):
        self.type = type
        self.path = path
        self.template = template

    def __getitem__(self, key: str):
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any):
        return setattr(self, key, value)

    def __contains__(self, key: str):
        return hasattr(self, key)
