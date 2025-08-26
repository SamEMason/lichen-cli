from pathlib import Path


def find_tool_root() -> Path:
    # Resolve file path of this file
    start = Path(__file__).resolve()

    # Work upwards looking for the root cli directory
    for parent in start.parents:
        # If the parent of the parent contains `pyproject.toml` return it's child: `lichen_cli`
        if (parent.parent / "pyproject.toml").exists():
            return parent

    raise RuntimeError(f"Tool root not found.")
