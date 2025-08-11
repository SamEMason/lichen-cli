from typer import Typer

app = Typer()


@app.command()
def dev():
    """Launch the lichen dev server"""
    print(f"dev server under construction...")
