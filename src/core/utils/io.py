import toml
from pathlib import Path
from typing import Any


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
    if not path.exists():
        raise FileNotFoundError(f"File not found {path}")
    return toml.load(path)


def write_toml(filepath: str | Path, content: dict[str, Any]):
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        toml.dump(content, file)


def load_template(filepath: str | Path) -> str | None:
    path = Path(filepath)
    if path.exists():
        with open(path) as file:
            return file.read()
