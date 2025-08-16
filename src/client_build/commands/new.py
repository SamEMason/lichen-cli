from typer import Typer


app = Typer()


@app.command()
def new(name: str):
    print(f"Scaffolding new project: {name}...")
