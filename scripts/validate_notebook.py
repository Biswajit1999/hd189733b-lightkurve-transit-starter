"""Offline structural validation for the self-contained Colab notebook."""

from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "HD189733b_Transit_Photometry.ipynb"


def python_source(cell: dict) -> str:
    """Remove Colab shell/magic lines before syntax validation."""
    lines = []
    for line in cell.get("source", []):
        if line.lstrip().startswith(("!", "%")):
            continue
        lines.append(line)
    return "".join(lines)


def main() -> None:
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
    for index, cell in enumerate(code_cells):
        source = python_source(cell)
        if source.strip():
            ast.parse(source, filename=f"code-cell-{index}")

    assert all(cell.get("execution_count") is None for cell in code_cells)
    assert all(not cell.get("outputs") for cell in code_cells)
    print(f"Notebook syntax valid: {len(code_cells)} code cells; outputs cleared.")


if __name__ == "__main__":
    main()
