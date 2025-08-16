from pathlib import Path


class Node:
    """Template file tree node"""

    def __init__(self, type: str, path: Path, template: Path):
        self.type = type
        self.path = path
        self.template = template
