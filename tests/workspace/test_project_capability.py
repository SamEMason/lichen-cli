from pathlib import Path
from pytest import MonkeyPatch

import core.context as ctx_mod
from core.utils.io import make_dir, make_file
from core.workspace import ProjectCapability, Workspace


def test_project_instantiates_as_type_project_capability():
    # Instantiate Workspace object
    ws = Workspace()

    # Assert Workspace.project is of type ProjectCapability
    assert isinstance(ws.project, ProjectCapability)


def test_project_new_method_is_callable():
    # Instantiate Workspace object
    ws = Workspace()

    # Assert Workspace.project_new method is callable
    assert callable(ws.project.new)


def test_project_new_method_creates_project_directory_inside_tmp_dir_when_root_is_cwd(
    monkeypatch: MonkeyPatch, tmp_path: Path
):
    # Force get_project_root() to return isolated tmp_path
    monkeypatch.setattr(ctx_mod, "find_project_root", lambda: tmp_path)
    monkeypatch.setattr(ctx_mod.Context, "cwd", property(lambda self: tmp_path))

    # Instantiate Workspace object
    ws = Workspace()

    # Create temporary scaffold.toml file within tmp_path
    scaffold_dir = ws.context.scaffold_dir
    scaffold_dir.mkdir(parents=True)

    template_path = tmp_path / "test.template"
    make_file(path=template_path, content="A test template.")

    # Minimal scaffold.toml that apply_nodes can handle
    ws.context.scaffold_file.write_text(
        """
        [default]
        version = "0.0.1"
        description = "Absolute MVP Lichen Stack file tree."
        nodes = [
            { type = "file", path = "test.md", template = "test.template" }
        ]

        """.strip()
    )

    # Invoke Workspace.project_new()
    project_name = "test_project"
    ws.project.new(project_name)

    assert ws.context.project_root == tmp_path
    assert ws.context.cwd == tmp_path

    # Assert Workspace.project_new creates tmp_dir
    assert tmp_path / ws.context.config.tmp_dir

    # Assert project directory exists inside tmp_dir
    assert (tmp_path / ws.context.config.tmp_dir / project_name).exists()


def test_project_new_method_creates_project_directory_without_tmp_dir_when_root_is_not_cwd(
    monkeypatch: MonkeyPatch, tmp_path: Path
):
    root_path = tmp_path / "root"
    cwd_path = tmp_path / "other"
    make_dir(root_path)
    make_dir(cwd_path)

    # Force get_project_root() to return isolated tmp_path
    monkeypatch.setattr(ctx_mod, "find_project_root", lambda: tmp_path / "root")
    monkeypatch.setattr(
        ctx_mod.Context, "cwd", property(lambda self: tmp_path / "other")
    )
    monkeypatch.chdir(cwd_path)

    # Instantiate Workspace object
    ws = Workspace()

    # Create temporary scaffold.toml file within tmp_path
    scaffold_dir = ws.context.scaffold_dir
    scaffold_dir.mkdir(parents=True)

    template_path = root_path / "test.template"
    make_file(path=template_path, content="A test template.")

    # Minimal scaffold.toml that apply_nodes can handle
    ws.context.scaffold_file.write_text(
        """
        [default]
        version = "0.0.1"
        description = "Absolute MVP Lichen Stack file tree."
        nodes = [
            { type = "file", path = "test.md", template = "test.template" }
        ]

        """.strip()
    )

    # Invoke Workspace.project_new()
    project_name = "test_project"
    ws.project.new(project_name)

    assert ws.context.project_root != tmp_path
    assert ws.context.cwd != tmp_path

    # Assert Workspace.project_new creates tmp_dir
    assert not (tmp_path / ws.context.config.tmp_dir).is_dir()

    # Assert project directory exists inside tmp_dir
    assert (cwd_path / project_name).exists()
