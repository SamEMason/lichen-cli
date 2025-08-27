from lichen_core.context import Context
from lichen_cli import utils
from lichen_cli.workspace.client import ClientCapability
from lichen_cli.workspace.project import ProjectCapability


class Workspace:
    def __init__(self, context: Context | None = None, autoload: bool = True):
        root = utils.find_tool_root()
        self.context = context or Context(project_root=root)
        self.autoload = autoload

        if autoload:
            self.context.load_config()

        self.client = ClientCapability(self.context)
        self.project = ProjectCapability(self.context)
