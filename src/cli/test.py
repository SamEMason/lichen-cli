from typer import Typer
from core.utils.tests import run_tests

app = Typer()


@app.command()
def test():
    """Run tests using `pytest`"""
    run_tests()