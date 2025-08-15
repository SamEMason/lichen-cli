from core.context import Context
from core.scaffold import Scaffolder
from core.workspace.base import BaseCapability


class ClientCapability(BaseCapability):
    def __init__(self, context: Context):
        super().__init__(context)
        self.scaffolder = Scaffolder(self.context)

    def build(self):
        pass
