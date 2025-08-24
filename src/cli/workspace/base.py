from dataclasses import dataclass

from core.context import Context


@dataclass
class BaseCapability:
    def __init__(self, context: Context):
        self.context = context