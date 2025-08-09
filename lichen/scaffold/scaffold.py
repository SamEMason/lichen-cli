from pathlib import Path
from lichen.config import Config
from lichen.utils.io import get_project_root, load_toml, make_dir, make_file


def scaffold_project(name: str):
    config = Config()

    # Project root directory
    root_dir = get_project_root()

    # Current working directory
    cwd = Path.cwd() 

    print(f"Root Directory: {root_dir}")
    print(f"Curr Directory: {cwd}")

    # Target directory  RENAME!!!!
    toml_file_base = root_dir
    print(f"Target Directory: {toml_file_base}")

    # Nest directory structure in temp/ in dev mode
    if config.mode == "dev":
        root_dir = cwd / config.temp_dir / name
        print(f"Root (modified): {root_dir}")

    # Load file tree nodes from scaffold.toml
    scaffold_file_path = f"{str(toml_file_base)}/{config.lichen_dir}/scaffold/scaffold.toml"
    scaffolding = load_toml(scaffold_file_path)

    nodes = scaffolding["default"][0]["nodes"]

    apply_nodes(nodes, root_dir)


def apply_nodes(nodes: list[dict[str, str]], location: Path):
    # Iterate through file tree nodes and create scaffolding
    for node in nodes:
        if node["type"] == "file":
            make_file(location / Path(node["path"]))
        elif node["type"] == "dir":
            make_dir(location / Path(node["path"]))