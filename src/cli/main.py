from typer import Typer
from cli.commands.dev import app as dev_app
from cli.commands.project import app as project_app
from cli.commands.service import app as service_app
from cli.commands.test import app as test_app


app = Typer()

app.add_typer(dev_app)
app.add_typer(project_app, name="project")
app.add_typer(service_app, name="service")
app.add_typer(test_app)
