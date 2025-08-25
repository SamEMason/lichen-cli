from pathlib import Path

from lichen_core.scaffold.node import Node


def test_node_instantiates_as_type_node():
    # Arguments for initializing Node object
    type = "file"
    path = Path("./test/path")
    template = Path("./test/template")

    # Instantiate Node object
    node = Node(type=type, path=path, template=template)

    # Assert Node object is of type Node
    assert isinstance(node, Node)


def test_node_initializes_with_constructed_properties():
    # Arguments for initializing Node object
    type = "file"
    path = Path("./test/path")
    template = Path("./test/template")

    # Instantiate Node object
    node = Node(type=type, path=path, template=template)

    # Assert Node.type is correct value
    assert isinstance(node.type, str)
    assert node.type == type

    # Assert Node.path is correct value
    assert isinstance(node.path, Path)
    assert node.path == path

    # Assert Node.template is correct value
    assert isinstance(node.template, Path)
    assert node.template == template
