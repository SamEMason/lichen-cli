from pathlib import Path
from lichen_cli.config import Config
from lichen_cli.utils.io import (
    get_project_root,
    load_template,
    load_toml,
    make_dir,
    make_file,
)


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
        target_directory = cwd / name

    # Load file tree nodes from scaffold.toml
    scaffold_file_path = toml_file_base / config.lichen_cli_dir / "scaffold/scaffold.toml"
    scaffolding = load_toml(scaffold_file_path)

    print(scaffold_file_path.resolve())

    # Nodes from scaffold.toml
    nodes = scaffolding["default"][0]["nodes"]

    # Create the project structure with nodes
    apply_nodes(nodes, target_directory)


def apply_nodes(nodes: list[dict[str, str]], location: Path):
    """Iteratively creates project structure at `location` using `nodes`"""
    root_dir = get_project_root()

    # Iterate through file tree nodes and create scaffolding
    for node in nodes:
        node_type = node["type"]
        relative_path = node["path"]
        target = location / relative_path

        if node_type == "dir":
            make_dir(target)

        elif node_type == "file":
            has_template = bool(node.get("template"))
            is_toml = Path(target).suffix == ".toml"

            # If file is of type TOML, load template contents and use write_toml
            if is_toml and has_template:
                content = load_template(root_dir / node["template"])
                if not content:
                    content = ""
                make_file(target, content=content)

            elif has_template:
                with open(root_dir / node["template"]) as file:
                    make_file(target, content=file.read())

            else:
                make_file(target)
                