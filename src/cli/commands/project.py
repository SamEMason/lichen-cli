from typer import Typer
from cli.workspace import Workspace

app = Typer()


@app.command()
def build():
    """Build the lichen app"""
    ws = Workspace()
    output = ws.project.build()
    print(output)


@app.command()
def destroy(name: str):
    """Destroy the specified lichen monorepo project"""
    ws = Workspace()
    output = ws.project.destroy(name)
    print(output)


@app.command()
def decimate():
    """Destroy the temp/ directory"""
    ws = Workspace()
    output = ws.project.decimate()
    print(output)


@app.command()
def new(name: str):
    """Create new lichen stack monorepo project"""
    ws = Workspace()
    ws.project.new(name)
