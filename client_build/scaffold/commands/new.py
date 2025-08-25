from typer import Typer

from lichen_cli.workspace import Workspace


app = Typer()


@app.command()
def new(name: str):
    ws = Workspace()
    ws.client.build(name)
