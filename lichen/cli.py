import typer
import shutil
from pathlib import Path
from .config import Config
from .scaffold import create_monorepo

app = typer.Typer()


@app.command()
def build():
    """Build the lichen app"""
    print(f"Build in progress...")


@app.command()
def destroy(name: str):
    config = Config()

    """Destroy the specified lichen monorepo project"""
    path = Path(f"{config.temp_dir}/{name}")
    if path.exists() and path.is_dir():
        shutil.rmtree(path)
        print(f"Project '{name}' destroyed.")
    else:
        print(f"Project '{name}' does not exist.")


@app.command()
def desolate():
    """Destroy the temp/ directory"""
    config = Config()
    temp_path = Path(config.temp_dir)

    if temp_path.exists() and temp_path.is_dir():
        shutil.rmtree(temp_path)
        print(f"Directory '{config.temp_dir}' destroyed.")
    else:
        print(f"Directory '{config.temp_dir}' does not exist.")


@app.command()
def dev():
    """Launch the lichen dev server"""
    print(f"lichen dev server running...")


@app.command()
def new(name: str):
    """Create new lichen stack monorepo project"""
    create_monorepo(name)


@app.command()
def service(command: str, names: list[str]):
    """Add or remove services from the Service Registry"""
    if command == "add":
        for name in names:
            print(f"Service: {name} added!")
    elif command == "remove":
        for name in names:
            print(f"Service: {name} removed!")
