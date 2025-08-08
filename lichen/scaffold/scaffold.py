from pathlib import Path
from lichen.config import Config
from lichen.utils.io import get_project_root, load_toml, make_dir, make_file


def scaffold_project(name: str):
    config = Config()

    # Project root directory
    root_dir = get_project_root()

    # Target directory  RENAME!!!!
    target_dir = root_dir

    # Nest directory structure in temp/ in dev mode
    if config.mode == "dev":
        root_dir = root_dir / config.temp_dir / name

    # Load file tree nodes from scaffold.toml
    scaffold_file_path = f"{str(target_dir)}/{config.lichen_dir}/scaffold/scaffold.toml"
    scaffolding = load_toml(scaffold_file_path)

    nodes = scaffolding["default"][0]["nodes"]

    # Iterate through file tree nodes and create scaffolding
    for node in nodes:
        if node["type"] == "file":
            make_file(root_dir / Path(node["path"]))
        elif node.type == "dir":
            make_dir(root_dir / Path(node["path"]))