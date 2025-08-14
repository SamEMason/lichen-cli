from core.context import Context
from core.workspace.client import ClientCapability
from core.workspace.project import ProjectCapability


class Workspace:
    def __init__(self, context: Context | None = None, autoload: bool = True):
        self.context = context or Context()
        self.autoload = autoload

        if autoload:
            self.context.load_config()

        self.client = ClientCapability(self.context)
        self.project = ProjectCapability(self.context)
