from pathlib import Path


def tool_root(name: str) -> Path:
    if name in TOOL_ROOTS:
        return TOOL_ROOTS[name]
    else:
        raise RuntimeError(f"Tool name {name} does not exist. Tool root not found.")


TOOL_ROOTS: dict[str, Path] = {
    "lichen": Path(__file__).resolve().parents[3],
    "lichen_cli": Path(__file__).resolve().parents[3] / "cli" / "lichen_cli",
    "scaffold": Path(__file__).resolve().parents[3] / "client_build" / "scaffold",
}
