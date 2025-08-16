from typer import Argument, Typer
from typing_extensions import Annotated

from core.config import CONFIG_FILENAME
from core.context import Context
from core.utils.io import load_toml

app = Typer()


@app.command()
def new(name: str):
    print(f"Scaffolding new project: {name}...")


@app.command()
def sync(name: Annotated[str, Argument()] = "ALL"):
    if name == "ALL":
        print(f"Syncing scaffolds...")
    else:
        print(f"Syncing scaffold: {name}...")


@app.command()
def version():
    ctx = Context()

    if ctx.client_build_dir is None:
        raise NotADirectoryError("Client_build directory not found.")

    path = ctx.client_build_dir / CONFIG_FILENAME
    data = load_toml(path)

    version = data.get("version", "unknown")

    print(f"Scaffold -- version {version}")
