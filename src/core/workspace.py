from core.context import Context


class Workspace:
    def __init__(self, context: Context | None = None, autoload: bool = True):
        self.context = context or Context()
        if autoload:
            self.context.load_config()
