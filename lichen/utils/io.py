import tomllib
from pathlib import Path
from typing import Any


def get_project_root() -> Path:
    start = Path(__file__).resolve()

    for parent in start.parents:
        if (parent / "pyproject.toml").exists():
            return parent

    raise RuntimeError("Project root not found")


def get_path(filepath: str) -> Path:
    root = get_project_root()
    return root / filepath


def make_dir(path: str | Path):
    p = Path(path)

    p.mkdir(parents=True, exist_ok=True)
    return p


def make_file(path: str | Path, content: str = "", overwrite: bool = False):
    # Get path from path argument
    p = Path(path)

    # Create ancestor directiries if necessary
    p.parent.mkdir(parents=True, exist_ok=True)

    # Return the path if the file already exists and overwrite is False
    if p.exists() and not overwrite:
        return p
    
    # Create the file with optionally inputted content
    with p.open("w") as file:
        file.write(content)

    return p


def load_toml(filepath: str, mode: str = "rb") -> dict[str, Any]:
    with open(filepath, mode) as file:
        return tomllib.load(file)
