from pathlib import Path
from typing import Optional, TypedDict

from core.context import Context
from core.registry import Registry, ScaffoldSet
from core.scaffold.node import Node
from core.utils.io import load_template, load_toml, make_dir, make_file


class MetaData(TypedDict):
    set_name: str
    version: str
    description: str


class ScaffoldNoneSet(TypedDict):
    set_name: str
    version: str | None
    description: str | None
    nodes: list[Node] | None


class Scaffolder:
    def __init__(
        self,
        context: Context,
        registry_path: Optional[str | Path] = None,
    ) -> None:
        self.context = context
        self.registry_path = registry_path
        self.meta: MetaData | None = None
        self.nodes: list[Node] = []

        self.selected_set: ScaffoldSet | ScaffoldNoneSet = ScaffoldNoneSet(
            set_name="default", version=None, description=None, nodes=None
        )

        # If registry_path is not passed in, default to core/scaffold/scaffold.toml
        if registry_path == None:
            self.registry_path = self.context.scaffold_file
        else:
            registry_path = Path(registry_path)
            self.registry_path = registry_path

        # Instantiate registry object
        self.registry = Registry(
            path=self.registry_path, selected_set=self.context.selected_set
        )

    def create(self, name: str, filepath: Optional[str | Path] = None):
        # Create root directory for project
        target = self._create_project_directory(name)

        # Load scaffolding nodes from scaffold.toml
        if filepath is not None:
            data_path = filepath
        else:
            data_path = self.context.scaffold_file

        scaffolding = load_toml(data_path)

        # NOTE: THIS LOGIC WILL NEED TO BE GENERALIZED WHEN CUSTOM SCAFFOLDS EXIST
        nodes = scaffolding["default"][0]["nodes"]

        if self.context.project_root is not None:
            # Build out project structure at target location with nodes
            self.apply_nodes(
                nodes=nodes, location=target, root_dir=self.context.project_root
            )

    def apply_nodes(self, nodes: list[dict[str, str]], location: Path, root_dir: Path):
        """Iteratively creates project structure at `location` using `nodes`"""
        # Iterate through file tree nodes and create scaffolding
        for node in nodes:
            node_type = node["type"]
            relative_path = node["path"]
            target = location / relative_path

            if node_type == "dir":
                make_dir(target)

            elif node_type == "file":
                has_template = bool(node.get("template"))
                is_toml = Path(target).suffix == ".toml"

                # If file is of type TOML, load template contents and use write_toml
                if is_toml and has_template:
                    content = load_template(root_dir / node["template"])
                    if not content:
                        content = ""
                    make_file(target, content=content)

                elif has_template:
                    with open(root_dir / node["template"]) as file:
                        make_file(target, content=file.read())

                else:
                    make_file(target)

    def _create_project_directory(self, name: str) -> Path:
        # Root and current working directory
        root = self.context.project_root
        cwd = self.context.cwd

        # Create a temporary directory around new project if cwd is the root
        if cwd == root:
            return cwd / self.context.config.tmp_dir / name
        return cwd / name

    def load(self, filepath: str | Path, set_name: str) -> str | None:
        path = Path(filepath)

        try:
            # Extract data from registry file at location: `filepath``
            extracted_data: ScaffoldSet = self.registry.load(path, select_set=set_name)

        except FileNotFoundError:
            # Raise error if registry is not found
            raise FileNotFoundError(f"Registry not found: {filepath}.")

        # Store meta data values in memory
        self.meta = {
            "set_name": extracted_data.get("set_name", ""),
            "version": extracted_data.get("version", ""),
            "description": extracted_data.get("description", ""),
        }

        # Select nodes from extracted registry data
        nodes = extracted_data.get("nodes")

        # Format and store selected nodes
        for node in nodes:
            type = node["type"]
            path = node["path"]
            template = node["template"]

            # Create new Node type to store node data
            new_node = Node(type=type, path=path, template=template)

            # Add node to nodes property stored in memory
            self.nodes.append(new_node)

    def save(self, filepath: str | Path, set: ScaffoldSet):
        path = Path(filepath)

        # Invoke Scaffolder.registry.save with scaffold set data
        self.registry.save(path, set)
