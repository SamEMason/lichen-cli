from pathlib import Path
from lichen.config import Config
from lichen.utils.io import get_project_root, load_toml, make_dir, make_file


def scaffold_project(name: str):
    """Top-level function for creating initial project scaffolding"""
    config = Config()

    # Project root directory
    root_dir = get_project_root()

    # Current working directory
    cwd = Path.cwd()

    # Target directory  RENAME!!!!
    toml_file_base = root_dir

    # Nest directory structure in temp/ in dev mode
    if config.mode == "dev":
        # Directory to create project structure
        target_directory = cwd / config.temp_dir / name
    else:
        target_directory = root_dir

    # Load file tree nodes from scaffold.toml
    scaffold_file_path = (
        f"{str(toml_file_base)}/{config.lichen_dir}/scaffold/scaffold.toml"
    )
    scaffolding = load_toml(scaffold_file_path)

    # Nodes from scaffold.toml
    nodes = scaffolding["default"][0]["nodes"]

    # Create the project structure with nodes
    apply_nodes(nodes, target_directory)


def apply_nodes(nodes: list[dict[str, str]], location: Path):
    """Iteratively creates project structure at `location` using `nodes`"""
    # Iterate through file tree nodes and create scaffolding
    for node in nodes:
        if node["type"] == "file":
            make_file(location / Path(node["path"]))
        elif node["type"] == "dir":
            make_dir(location / Path(node["path"]))
