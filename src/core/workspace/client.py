from core.scaffold import Scaffolder
from core.workspace.base import BaseCapability


class ClientCapability(BaseCapability):
    scaffolder = Scaffolder()

    def build(self):
        pass