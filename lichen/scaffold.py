from pathlib import Path


def create_monorepo(name: str):
    base = Path(name)
    base.mkdir(parents=True, exist_ok=True)
    (base / "services").mkdir()
    
    (base / "shared").mkdir()
    (base / "shared" / "utils.py").write_text(
        'print("utils.py")\n'
    )
    
    (base / "services" / "gateway").mkdir(parents=True)
    (base / "services" / "gateway" / "main.py").write_text(
        'print("gateway lives on")\n'
    )
    
    (base / "README.md").write_text(f"# {name} monorepo\n")
    (base / ".gitignore").write_text("")
