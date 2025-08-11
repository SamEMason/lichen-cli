import typer
from lichen_cli.cli.dev import app as dev_app
from lichen_cli.cli.project import app as project_app
from lichen_cli.cli.service import app as service_app
from lichen_cli.cli.test import app as test_app

app = typer.Typer()

app.add_typer(dev_app)
app.add_typer(project_app, name="project")
app.add_typer(service_app, name="service")
app.add_typer(test_app)


