from core.context import Context
from core.scaffold import Scaffolder
from core.workspace.base import BaseCapability


class ClientCapability(BaseCapability):
    def __init__(self, context: Context):
        super().__init__(context)
        if self.context.client_build_dir is None:
            raise ValueError("Client build `scaffolds` directory is of type None.")

        registry_path = self.context.client_build_dir / ".scaffold" / "registry.toml"
        self.scaffolder = Scaffolder(self.context, registry_path=registry_path)

    def build(self, name: str):
        print(f"Building `{name}` in progress...")

        self.scaffolder.create(name)
