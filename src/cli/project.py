from typer import Typer
from core.workspace import Workspace

app = Typer()


@app.command()
def build():
    """Build the lichen app"""
    ws = Workspace()
    output = ws.project_build()
    print(output)


@app.command()
def destroy(name: str):
    """Destroy the specified lichen monorepo project"""
    ws = Workspace()
    output = ws.project_destroy(name)
    print(output)


@app.command()
def decimate():
    """Destroy the temp/ directory"""
    ws = Workspace()
    output = ws.project_decimate()
    print(output)


@app.command()
def new(name: str):
    """Create new lichen stack monorepo project"""
    ws = Workspace()
    ws.project_new(name)
