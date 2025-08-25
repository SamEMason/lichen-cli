from pathlib import Path
from typing import Optional, Sequence, TypedDict

from lichen_core.context import Context
from lichen_core.registry import Registry, ScaffoldSet
from lichen_core.scaffold.node import Node
from lichen_core.utils.discovery import tool_root
from lichen_core.utils.io import load_template, make_dir, make_file


class MetaData(TypedDict):
    set_name: str
    version: str
    description: str


class PreloadedScaffoldSet(TypedDict):
    set_name: str
    version: str | None
    description: str | None
    nodes: list[Node] | None


class Scaffolder:
    def __init__(self, context: Context, registry_path: Optional[Path] = None) -> None:
        self.context: Context = context
        self.registry_path: Optional[Path] = None
        self.selected_set: ScaffoldSet | PreloadedScaffoldSet = PreloadedScaffoldSet(
            set_name="default", version=None, description=None, nodes=None
        )

        # Create temporary scaffold.toml file within tmp_path
        if registry_path is None:
            if self.context.project_root is None:
                raise ValueError("Project root is not initialized.")

            self.registry_path = (
                self.context.project_root / ".scaffold" / "registry.toml"
            )

        else:
            self.registry_path = registry_path

        # Instantiate registry object
        self.registry = Registry(
            path=self.registry_path, selected_set=self.context.selected_set
        )

    def create(self, name: str):
        # Create root directory for project
        target = self._create_project_directory(name)

        # Load the selected set from the registry into memory
        set_name = self.selected_set["set_name"]
        self.load(set_name=set_name)

        # Extract the nodes from the selected set in memory
        nodes = self.selected_set["nodes"]

        # Raise a ValueError if the nodes we're loaded as None
        if nodes is None:
            raise ValueError("Nodes were not loaded properly.")

        if self.context.project_root is not None:
            # Build out project structure at target location with nodes
            self.apply_nodes(
                nodes=nodes, location=target, root_dir=self.context.project_root
            )

    def apply_nodes(self, nodes: Sequence[Node], location: Path, root_dir: Path):
        """Iteratively creates project structure at `location` using `nodes`"""
        # Iterate through file tree nodes and create scaffolding
        for node in nodes:
            node_type = node["type"]
            relative_path = node["path"]

            ###### NOTE: SHOULD VALIDATE THAT THE PATHS ARE RELATIVE HERE

            # Resolve target path from root scaffold directory
            target = location / relative_path

            # If node type is "dir" create a directory
            if node_type == "dir":
                make_dir(target)

            # Else if node type is "file" create a file
            elif node_type == "file":
                has_template = bool(node["template"])
                is_toml = Path(target).suffix == ".toml"

                # If file is of type TOML load template contents and use write_toml
                if is_toml and has_template:
                    content = load_template(root_dir / node["template"])

                    # If the template is empty use an empty string as content
                    if not content:
                        content = ""
                    make_file(target, content=content)

                # If file is not of type TOML but has template create file copying from template file
                elif has_template:
                    with open(root_dir / node["template"]) as file:
                        make_file(target, content=file.read())

                # In all other cases create an empty file
                else:
                    make_file(target)

    def _create_project_directory(self, name: str) -> Path:
        # Root and current working directory
        root = tool_root("lichen")
        cwd = self.context.working_root

        # Create a temporary directory around new project if cwd is the root
        if cwd == root:
            return cwd / self.context.config.tmp_dir / name
        return cwd / name

    def load(self, set_name: str) -> str | None:
        if self.registry_path is None:
            raise ValueError("Registry path does not exist.")

        # Ensure registry_path is of type Path
        path = Path(self.registry_path)

        # Extract data from registry file at location: `filepath``
        extracted_data: ScaffoldSet = self.registry.load(path, select_set=set_name)

        # Store meta data values in memory
        self.selected_set["set_name"] = extracted_data.get("set_name")
        self.selected_set["version"] = extracted_data.get("version")
        self.selected_set["description"] = extracted_data.get("description")

        # Store nodes list into memory
        self.selected_set["nodes"] = extracted_data.get("nodes")

    def save(self, set: ScaffoldSet):
        if self.registry_path is None:
            raise ValueError("Registry path does not exist.")

        # Invoke Scaffolder.registry.save with scaffold set data
        self.registry.save(self.registry_path, set)
