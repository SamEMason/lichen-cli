from core.context import Context
from core.scaffold import Scaffolder
from cli.workspace.base import BaseCapability


class ClientCapability(BaseCapability):
    def __init__(self, context: Context):
        super().__init__(context)

        self.scaffolder = Scaffolder(self.context)

    def build(self, name: str):
        print(f"Building `{name}` in progress...")

        self.scaffolder.create(name)
