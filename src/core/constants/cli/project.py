from pathlib import Path


# Static
BUILD_OUTPUT = "build process under construction..."


# Dynamic
def decimate_success(tmp_dir: str | Path):
    return f"Directory '{tmp_dir}' destroyed."


def decimate_fail(tmp_dir: str | Path):
    return f"Directory '{tmp_dir}' does not exist."
