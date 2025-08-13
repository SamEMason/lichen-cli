from dataclasses import dataclass

from core.context import Context


@dataclass
class BaseCapability:
    context: Context
