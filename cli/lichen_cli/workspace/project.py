from shutil import rmtree

from lichen_cli.workspace.base import BaseCapability
from lichen_core.context import Context
from lichen_core.scaffold import Scaffolder
from lichen_core.utils.discovery import is_in_project_dir


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
        cwd = self.context.working_root
        tmp_dir = self.context.config.tmp_dir
        temp_path = cwd / tmp_dir

        if temp_path and temp_path.exists() and temp_path.is_dir():
            rmtree(temp_path)

            # Reset project name to empty string in config
            self.context.save_config("project_name", "")

            return f"Directory: {tmp_dir} successfully decimated."
        else:
            return f"Directory: {tmp_dir} was not found."

    def destroy(self, name: str):
        """Destroy the specified lichen monorepo project"""  # NOTE: REFACTOR -> WRAP RMTREE
        # Get current working directory `cwd`
        cwd = self.context.working_root

        # If `cwd` is within lichen project repo prepend tmp_dir to target path
        if is_in_project_dir(cwd):
            target = f"{self.context.config.tmp_dir}/{name}"
        else:
            target = name

        # Append target path to `cwd`
        path = self.context.working_root / target

        # If the path exists and is a directory destroy scaffold
        if path.exists() and path.is_dir():
            rmtree(path)

            # Reset project name to empty string in config
            self.context.save_config("project_name", "")

            return f"Project '{name}' destroyed."
        else:
            return f"Project '{name}' does not exist."
