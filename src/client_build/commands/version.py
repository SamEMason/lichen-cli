from typer import Typer

from core.config import CONFIG_FILENAME
from core.context import Context
from core.utils.io import load_toml


app = Typer()


@app.command()
def version():
    ctx = Context()

    if ctx.client_build_dir is None:
        raise NotADirectoryError("Client_build directory not found.")

    path = ctx.client_build_dir / CONFIG_FILENAME
    data = load_toml(path)

    version = data.get("version", "unknown")

    print(f"Scaffold -- version {version}")
