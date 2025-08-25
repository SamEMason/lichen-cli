from typer import Typer


app = Typer()


@app.command("list")
@app.command("ls")
def list():
    print("Scaffolds")
    print("scaffold_1")
    print("scaffold_2")
    print("scaffold_3")
    print("scaffold_4")
