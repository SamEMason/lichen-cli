from typer import Typer

from core.context import Context
from core.utils.io import load_toml


app = Typer()


@app.command()
def version():
    ctx = Context()

    if ctx.project_root is None:
        raise ValueError("Project root was not initialized.")

    meta_file = ctx.project_root / ".scaffold" / "meta.toml"

    data = load_toml(meta_file)

    version = data.get("version", "unknown")

    print(f"Scaffold -- version {version}")
