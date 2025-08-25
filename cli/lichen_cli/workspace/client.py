from lichen_core.context import Context
from lichen_core.scaffold.scaffolder import Scaffolder
from lichen_cli.workspace.base import BaseCapability


class ClientCapability(BaseCapability):
    def __init__(self, context: Context):
        super().__init__(context)

        self.scaffolder = Scaffolder(self.context)

    def build(self, name: str):
        print(f"Building `{name}` in progress...")

        self.scaffolder.create(name)
