from pathlib import Path
from shutil import rmtree
from typer import Typer
from core.config import Config
from core.workspace import Workspace

app = Typer()


@app.command()
def build():
    """Build the lichen app"""
    print(f"build process under construction...")


@app.command()
def destroy(name: str):
    """Destroy the specified lichen monorepo project"""
    config = Config()
    path = Path(f"{config.tmp_dir}/{name}")

    if path.exists() and path.is_dir():
        rmtree(path)
        print(f"Project '{name}' destroyed.")
    else:
        print(f"Project '{name}' does not exist.")


@app.command()
def decimate():
    """Destroy the temp/ directory"""
    config = Config()
    temp_path = Path(config.tmp_dir)

    if temp_path.exists() and temp_path.is_dir():
        rmtree(temp_path)
        print(f"Directory '{config.tmp_dir}' destroyed.")
    else:
        print(f"Directory '{config.tmp_dir}' does not exist.")


@app.command()
def new(name: str):
    """Create new lichen stack monorepo project"""
    ws = Workspace()

    ws.project_new(name)
