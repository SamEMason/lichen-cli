from pathlib import Path


def is_in_project_dir(working_dir: Path) -> bool:
    # If working directory is `lichen/` return True
    if working_dir.name == "lichen":
        return True

    # Work upwards looking for the root cli directory
    for parent in working_dir.parents:
        # If the parent of the parent contains `pyproject.toml` return it's child: `lichen_cli`
        if parent.name == "lichen":
            return True

    return False
