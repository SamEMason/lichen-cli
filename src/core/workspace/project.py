from pathlib import Path
from shutil import rmtree

from core.constants.cli.project import BUILD_OUTPUT, decimate_fail, decimate_success

from core.scaffold import Scaffolder
from core.utils.io import load_toml
from core.workspace.base import BaseCapability


class ProjectCapability(BaseCapability):
    scaffolder = Scaffolder()

    def build(self) -> str:
        return BUILD_OUTPUT

    def new(self, name: str):
        # Create root directory for project
        target = self._create_project_directory(name)

        # Load scaffolding nodes from scaffold.toml
        scaffolding = load_toml(self.context.scaffold_file)

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
            return decimate_success(tmp_dir)
        else:
            return decimate_fail(tmp_dir)

    def destroy(self, name: str):
        """Destroy the specified lichen monorepo project"""  # NOTE: REFACTOR -> WRAP RMTREE
        cwd = self.context.cwd
        root = self.context.project_root

        if cwd == root:
            target = f"{self.context.config.tmp_dir}/{name}"
        else:
            target = name

        path = self.context.path_from_cmd(target)

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
