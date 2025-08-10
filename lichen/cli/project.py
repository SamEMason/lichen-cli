from pathlib import Path
from shutil import rmtree
from typer import Typer
from lichen.config import Config
from lichen.scaffold import scaffold_project


app = Typer()


@app.command()
def build():
    """Build the lichen app"""
    print(f"build process under construction...")


@app.command()
def destroy(name: str):
    """Destroy the specified lichen monorepo project"""
    config = Config()
    path = Path(f"{config.temp_dir}/{name}")

    if path.exists() and path.is_dir():
        rmtree(path)
        print(f"Project '{name}' destroyed.")
    else:
        print(f"Project '{name}' does not exist.")


@app.command()
def decimate():
    """Destroy the temp/ directory"""
    config = Config()
    temp_path = Path(config.temp_dir)

    if temp_path.exists() and temp_path.is_dir():
        rmtree(temp_path)
        print(f"Directory '{config.temp_dir}' destroyed.")
    else:
        print(f"Directory '{config.temp_dir}' does not exist.")


@app.command()
def new(name: str):
    """Create new lichen stack monorepo project"""
    scaffold_project(name)
