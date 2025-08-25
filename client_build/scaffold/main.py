from typer import Typer

from client_build.commands.list import app as list_app
from client_build.commands.new import app as new_app
from client_build.commands.sync import app as sync_app
from client_build.commands.version import app as version_app


app = Typer()

app.add_typer(list_app)
app.add_typer(new_app)
app.add_typer(sync_app)
app.add_typer(version_app)
