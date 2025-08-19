from dataclasses import dataclass
from pathlib import Path
from typing import cast

from core.scaffold import Node
from core.scaffold import SelectedSet
from core.utils.io import load_toml


@dataclass
class Registry:
    path: str | Path
    selected_set: str

    def load(self, filepath: Path, select_set: str) -> SelectedSet:
        # Load data from filepath
        data = load_toml(filepath)

        # Check if selected set is a valid key
        if select_set not in data:
            raise KeyError(f"Scaffold set `{select_set}` not found.")

        # Select the selected set from registry data
        set = data[select_set]

        # Extract and normalize meta data
        version = cast(str, set.get("version"))
        description = cast(str, set.get("description"))
        raw_nodes: list[Node] = set.get("nodes")

        # Extract and normalize nodes as Node type objects
        nodes: list[Node] = [
            Node(type=node["type"], path=node["path"], template=node["template"])
            for node in raw_nodes
        ]

        # Return SelectedSet object
        return {
            "set_name": select_set,
            "version": version,
            "description": description,
            "nodes": nodes,
        }
