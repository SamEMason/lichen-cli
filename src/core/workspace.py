from pathlib import Path

from core.context import Context
from core.scaffold import Scaffolder
from core.utils.io import load_toml


class Workspace:
    def __init__(self, context: Context | None = None, autoload: bool = True):
        self.context = context or Context()
        self.scaffolder = Scaffolder()

        if autoload:
            self.context.load_config()

    def project_new(self, name: str):
        # Create root directory for project
        target = self._create_project_directory(name)

        # Resolve filepath for scaffold.toml
        scaffold_file_path = self.context.scaffold_dir / "scaffold.toml"

        # Load scaffolding nodes from scaffold.toml
        scaffolding = load_toml(scaffold_file_path)

        # NOTE: THIS LOGIC WILL NEED TO BE GENERALIZED WHEN CUSTOM SCAFFOLDS EXIST
        nodes = scaffolding["default"][0]["nodes"]

        if self.context.project_root is not None:
            # Build out project structure at target location with nodes
            self.scaffolder.apply_nodes(
                nodes=nodes, location=target, root_dir=self.context.project_root
            )

    def _create_project_directory(self, name: str) -> Path:
        # Root and current working directory
        root = self.context.project_root
        cwd = self.context.cwd

        # Create a temporary directory around new project if cwd is the root
        if cwd == root:
            return cwd / self.context.config.tmp_dir / name
        return cwd / name
