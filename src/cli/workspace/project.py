from shutil import rmtree

from core.constants.cli.project import BUILD_OUTPUT, decimate_fail, decimate_success
from core.context import Context
from core.scaffold import Scaffolder
from cli.workspace.base import BaseCapability


class ProjectCapability(BaseCapability):
    def __init__(self, context: Context):
        super().__init__(context)
        self.scaffolder = Scaffolder(self.context)

    def build(self) -> str:
        return BUILD_OUTPUT

    def new(self, name: str):
        self.scaffolder.create(name)

    def decimate(self) -> str:
        """Absolutely decimate the tmp_dir/ directory"""
        assert self.context.project_root is not None
        tmp_dir = self.context.config.tmp_dir
        temp_path = self.context.project_root / tmp_dir

        if temp_path and temp_path.exists() and temp_path.is_dir():
            rmtree(temp_path)
            return decimate_success(tmp_dir)
        else:
            return decimate_fail(tmp_dir)

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
