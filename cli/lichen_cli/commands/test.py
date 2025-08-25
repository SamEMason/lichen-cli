from typer import Typer
import subprocess

app = Typer()


@app.command()
def test():
    """Run tests using `pytest`"""
    run_tests()


def run_tests():
    """Run tests using `pytest`"""
    subprocess.run(["pytest", "-s"])
