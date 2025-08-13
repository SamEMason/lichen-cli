from pathlib import Path

from core.utils.io import load_template, make_dir, make_file


class Scaffolder:
    def apply_nodes(self, nodes: list[dict[str, str]], location: Path, root_dir: Path):
        """Iteratively creates project structure at `location` using `nodes`"""
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
                    content = load_template(
                        root_dir / node["template"]
                    )
                    if not content:
                        content = ""
                    make_file(target, content=content)

                elif has_template:
                    with open(root_dir / node["template"]) as file:
                        make_file(target, content=file.read())

                else:
                    make_file(target)
