from shutil import rmtree

from lichen_cli.workspace.base import BaseCapability
from lichen_core.context import Context
from lichen_core.scaffold import Scaffolder
from lichen_core.utils.discovery import tool_root


class ProjectCapability(BaseCapability):
    def __init__(self, context: Context):
        super().__init__(context)
        self.scaffolder = Scaffolder(self.context)

    def build(self) -> str:
        return "Build process in progress..."

    def new(self, name: str):
        self.scaffolder.create(name)

    def decimate(self) -> str:
        """Absolutely decimate the tmp_dir/ directory"""
        root = tool_root("lichen")
        tmp_dir = self.context.config.tmp_dir
        temp_path = root / tmp_dir

        if temp_path and temp_path.exists() and temp_path.is_dir():
            rmtree(temp_path)
            return f"Directory: {tmp_dir} successfully decimated."
        else:
            return f"Directory: {tmp_dir} was not found."

    def destroy(self, name: str):
        """Destroy the specified lichen monorepo project"""  # NOTE: REFACTOR -> WRAP RMTREE
        cwd = self.context.working_root
        root = self.context.project_root

        if cwd == root:
            target = f"{self.context.config.tmp_dir}/{name}"
        else:
            target = name

        path = self.context.working_root / target

        if path.exists() and path.is_dir():
            rmtree(path)
            return f"Project '{name}' destroyed."
        else:
            return f"Project '{name}' does not exist."
