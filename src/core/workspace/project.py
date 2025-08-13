from pathlib import Path
from shutil import rmtree

from core.scaffold import Scaffolder
from core.utils.io import load_toml
from core.workspace.base import BaseCapability


class ProjectCapability(BaseCapability):
    scaffolder = Scaffolder()

    def build(self) -> str:
        return "build process under construction..."

    def new(self, name: str):
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

    def decimate(self) -> str:
        """Absolutely decimate the tmp_dir/ directory"""
        temp_path = self.context.temporary_dir
        tmp_dir = self.context.config.tmp_dir

        if temp_path and temp_path.exists() and temp_path.is_dir():
            rmtree(temp_path)
            return f"Directory '{tmp_dir}' destroyed."
        else:
            return f"Directory '{tmp_dir}' does not exist."

    def destroy(self, name: str):
        """Destroy the specified lichen monorepo project"""
        path = Path(name)

        if path.exists() and path.is_dir():
            rmtree(path)
            return f"Project '{name}' destroyed."
        else:
            return f"Project '{name}' does not exist."

    def _create_project_directory(self, name: str) -> Path:
        # Root and current working directory
        root = self.context.project_root
        cwd = self.context.cwd

        # Create a temporary directory around new project if cwd is the root
        if cwd == root:
            return cwd / self.context.config.tmp_dir / name
        return cwd / name
