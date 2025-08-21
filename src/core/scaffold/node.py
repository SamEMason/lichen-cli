from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Node:
    """Template file tree node"""

    type: str
    path: Path
    template: Path

    def __getitem__(self, key: str):
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any):
        return setattr(self, key, value)

    def __contains__(self, key: str):
        return hasattr(self, key)
