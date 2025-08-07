import os
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


def make_dir(name: str):
    if not Path(name).exists():
        try:
            os.mkdir(name)
            print(f"Directory `{name}' created successfully.")
        except PermissionError:
            print(f"Permission denied: Unable to create '{name}'.")
        except Exception as e:
            print(f"An error has occurred: {e}")


def make_file(filename: str, mode: str = "w", content: str = ""):
    if "r" in mode:
        raise ValueError("Cannot use read mode to make a file")

    if not get_path(filename).exists():
        with open(filename, mode) as file:
            file.write(content)


def load_toml(filepath: str, mode: str = "rb") -> dict[str, Any]:
    with open(filepath, mode) as file:
        return tomllib.load(file)
