import subprocess

from core.utils.discovery import find_project_root


def run_tests():
    """Run tests using `pytest`"""
    subprocess.run(["pytest"])


def get_test_data(filename: str):
    """Retrieve absolute filepath for test data files"""
    root = find_project_root()
    relative_path = "tests/test_data"
    target = root / relative_path / filename

    # Raise FileNotFoundError if file doesn't exist at this path
    if not target.exists():
        raise FileNotFoundError(f"File {filename} does not exist at {target}.")

    # Raise IsADirectoryError if the filename argument is a directory path
    if target.is_dir():
        raise IsADirectoryError(
            f"Filepath argument {filename} is a directory path not a filepath"
        )

    # Otherwise return the target path
    return target
