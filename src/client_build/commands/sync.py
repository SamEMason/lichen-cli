from typer import Argument, Typer
from typing_extensions import Annotated


app = Typer()


@app.command()
def sync(name: Annotated[str, Argument()] = "ALL"):
    if name == "ALL":
        print(f"Syncing scaffolds...")
    else:
        print(f"Syncing scaffold: {name}...")
