from typer import Typer

app = Typer()


@app.command()
def service(command: str, names: list[str]):
    """Add or remove services from the Service Registry"""
    if command == "add":
        for name in names:
            print(f"Service: {name} added!")
    elif command == "remove":
        for name in names:
            print(f"Service: {name} removed!")
