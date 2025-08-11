from typer import Typer
from lichen_cli.utils.tests import run_tests

app = Typer()


@app.command()
def test():
    """Run tests using `pytest`"""
    run_tests()