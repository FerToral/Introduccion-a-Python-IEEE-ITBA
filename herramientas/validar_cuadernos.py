"""Comprueba estructura y sintaxis sin ejecutar los cuadernos."""

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validar(path):
    notebook = json.loads(path.read_text(encoding="utf-8"))
    counts = {"celdas": len(notebook["cells"]), "codigo": 0, "markdown": 0,
              "magias": 0, "sin_implementacion": 0}
    errors = []
    for cell in notebook["cells"]:
        if cell["cell_type"] == "markdown":
            counts["markdown"] += 1
            continue
        counts["codigo"] += 1
        source = "".join(cell["source"])
        lines = source.splitlines()
        # Comandos de Colab/IPython: no son sintaxis Python de un módulo .py.
        magic = any(line.lstrip().startswith(("!", "%")) for line in lines)
        if magic:
            counts["magias"] += 1
        python_source = "\n".join(
            "pass  # comando IPython" if line.lstrip().startswith(("!", "%")) else line
            for line in lines
        )
        try:
            tree = ast.parse(python_source, filename=f"{path.name}:{cell['id']}")
            if not tree.body:
                counts["sin_implementacion"] += 1
        except SyntaxError as error:
            errors.append({"celda": cell["id"], "error": str(error)})
        if cell.get("outputs") or cell.get("execution_count") is not None:
            errors.append({"celda": cell["id"], "error": "Salidas o ejecución guardadas"})
    counts["errores"] = errors
    return counts


def main():
    results = {str(path.relative_to(ROOT)): validar(path)
               for path in sorted((ROOT / "clases").glob("*/*.ipynb"))}
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return int(any(result["errores"] for result in results.values()))


if __name__ == "__main__":
    raise SystemExit(main())
