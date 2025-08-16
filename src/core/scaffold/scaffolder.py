from pathlib import Path
from typing import Optional

from core.context import Context
from core.scaffold.node import Node
from core.utils.io import load_template, load_toml, make_dir, make_file


class Scaffolder:
    def __init__(
        self, context: Context, template_file: str | Path | None = None
    ) -> None:
        self.context = context
        self.nodes: list[Node] | None = None

        # If template_file is not passed in, default to core/scaffold/scaffold.toml
        if template_file == None:
            self.template_file = self.context.scaffold_file
        else:
            template_file = Path(template_file)
            self.template_file = template_file

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

    def read_nodes(self, filepath: str | Path) -> str | None:
        path = Path(filepath)
        if path.exists():
            with open(path) as file:
                return file.read()

    def write_nodes(self, nodes: dict[str, list[Node]]):
        print(nodes)
