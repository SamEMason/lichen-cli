import toml
from pathlib import Path
from typing import Any


def get_project_root() -> Path:
    start = Path(__file__).resolve()

    for parent in start.parents:
        if (parent / "pyproject.toml").exists():
            return parent

    raise RuntimeError("Project root not found")


def get_path(filepath: str | Path) -> Path:
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


def load_toml(filepath: str | Path) -> dict[str, Any]:
    path = Path(filepath)
    return toml.load(path) if path.exists() else {}


def write_toml(filepath: str | Path, content: dict[str, str]):
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        toml.dump(content, file)
