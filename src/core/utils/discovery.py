from pathlib import Path

def find_project_root() -> Path:
    start = Path(__file__).resolve()

    for parent in start.parents:
        if (parent / "pyproject.toml").exists():
            return parent

    raise RuntimeError("Project root not found")