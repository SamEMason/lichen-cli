import os
from pathlib import Path


# Creating Lichen Stack Structure

def _make_dir(name: str):
    if not Path(name).exists():
        try:
            os.mkdir(name)
            print(f"Directory `{name}' created successfully.")
        except PermissionError:
            print(f"Permission denied: Unable to create '{name}'.")
        except Exception as e:
            print(f"An error has occurred: {e}")


def make_temp_dir():
    _make_dir("temp")


def make_root_dir(name: str):
    _make_dir(name)
