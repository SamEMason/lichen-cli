from pathlib import Path
from dataclasses import dataclass


@dataclass
class Registry:
    path: str | Path
    selected_set: str
