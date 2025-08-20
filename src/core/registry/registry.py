from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypedDict

from core.scaffold import Node
from core.utils.io import load_toml


class SelectedSet(TypedDict):
    set_name: str
    version: str
    description: str
    nodes: list[Node]


@dataclass
class Registry:
    path: str | Path
    selected_set: str

    def _read(self, filepath: Path) -> dict[str, Any]:
        """Read raw data from TOML file"""
        # Raise exception if file not found at `filepath`
        if not filepath.exists():
            raise FileNotFoundError(f"File {filepath} does not exist.")

        # Return loaded data from filepath
        return load_toml(filepath)

    def load(self, filepath: Path, select_set: str) -> SelectedSet:
        # Read raw registry data
        data = self._read(filepath=filepath)

        # Extract selected set from registry data
        set = data[select_set]

        version = set.get("version")
        description = set.get("description")
        raw_nodes: list[Node] = set.get("nodes")

        # Extract and normalize nodes as Node type objects
        nodes: list[Node] = [
            Node(type=node["type"], path=node["path"], template=node["template"])
            for node in raw_nodes
        ]

        # Return SelectedSet object
        return SelectedSet(
            set_name=select_set,
            version=version,
            description=description,
            nodes=nodes,
        )

    def save(self, filepath: str | Path, set: SelectedSet):
        path = Path(filepath)

        # Raise error if set_name is an empty string
        if set["set_name"] is "":
            raise ValueError("Property `set_name` must contain at least one character.")

        # Load data from filepath
        