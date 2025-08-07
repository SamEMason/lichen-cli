from typer import Typer

app = Typer()


@app.command()
def add(names: list[str]):
    for name in names:
        print(f"Service: {name} added!")


@app.command()
def remove(names: list[str]):
    for name in names:
        print(f"Service: {name} removed!")
