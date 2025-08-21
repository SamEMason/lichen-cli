from dataclasses import dataclass
from pathlib import Path
from typing import Any, TextIO, TypedDict

from core.scaffold import Node
from core.utils.io import load_toml


class ScaffoldSet(TypedDict):
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

    def _write(self, filepath: Path, data: dict[str, ScaffoldSet]):
        # Open registry file for overwriting
        with filepath.open("w", encoding="utf-8") as f:
            # Iterate through each scaffold set in `data` argument
            for set, props in data.items():
                # Extract meta data and nodes from scaffold set data
                version = props.get("version")
                description = props.get("description")
                nodes = props.get("nodes")

                # Convert extracted nodes into Node objects
                current_node_list = [
                    Node(
                        type=node["type"], path=node["path"], template=node["template"]
                    )
                    for node in nodes
                ]

                # Package the current scaffold set data into a ScaffoldSet object
                current_set = ScaffoldSet(
                    set_name=set,
                    version=version,
                    description=description,
                    nodes=current_node_list,
                )

                # Invoke _write_registry_set to write the current set in proper format
                self._write_registry_set(set=current_set, file=f)

    def _write_registry_set(self, file: TextIO, set: ScaffoldSet):
        # Write the scaffold set name
        file.write(f'["{set["set_name"]}"]\n')

        # Write the scaffold set meta data
        file.write(f'version = "{set["version"]}"\n')
        file.write(f'description = "{set["description"]}"\n')

        # Write in nodes list opening bracket
        file.write(f"nodes = [\n")

        # Iterate through nodes writing each object manually
        for node in set["nodes"]:
            file.write("\t{ ")
            file.write(
                f'type = "{node["type"]}", path = "{node["path"]}", template = "{node["template"]}"'
            )
            file.write(" },\n")

        # Close node list bracket and create space below set
        file.write("]\n\n")

    def load(self, filepath: Path, select_set: str) -> ScaffoldSet:
        # Read raw registry data
        data = self._read(filepath=filepath)

        # Extract selected set from registry data
        set = data[select_set]

        # Get each property within the selected set
        version = set.get("version")
        description = set.get("description")
        raw_nodes: list[Node] | None = set.get("nodes")

        # Raise exception if raw nodes is NoneType
        if raw_nodes is None:
            raise ValueError("Registry data could not be loaded.")

        # Extract and normalize nodes as Node type objects
        nodes: list[Node] = [
            Node(type=node["type"], path=node["path"], template=node["template"])
            for node in raw_nodes
        ]

        # Return ScaffoldSet object
        return ScaffoldSet(
            set_name=select_set,
            version=version,
            description=description,
            nodes=nodes,
        )

    def save(self, registry_path: str | Path, set: ScaffoldSet):
        registry_path = Path(registry_path)
        # Raise error if set_name is an empty string
        if set["set_name"] == "":
            raise ValueError("Property `set_name` must contain at least one character.")

        # Read data from registry_path
        data = self._read(registry_path)

        # Update loaded data dictionary with new selected set data
        set_name = set["set_name"]

        if data.get(set_name) is None:
            raise KeyError(f"Set name `{set_name}` is not a valid key.")

        # Update selected set data
        data[set_name] = set

        # Overwrite data back onto registry_path with proper formatting
        self._write(filepath=registry_path, data=data)
