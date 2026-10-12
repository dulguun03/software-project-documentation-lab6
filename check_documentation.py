"""Internal lab verifier: check API coverage and scan authored Python comments."""
import ast
import io
import json
from pathlib import Path
import re
import tokenize

ROOT = Path(__file__).resolve().parents[1]


def main():
    """Run this internal command; it is excluded from the supported API."""
    symbols, failures = [], []
    for relative in ["server.py", "samples/client.py"]:
        tree = ast.parse((ROOT / relative).read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and not node.name.startswith("_"):
                targets = [(node.name, node)]
                if isinstance(node, ast.ClassDef):
                    targets += [(node.name + "." + child.name, child) for child in node.body
                                if isinstance(child, ast.FunctionDef)
                                and (not child.name.startswith("_") or child.name == "__init__")]
                for name, target in targets:
                    doc = ast.get_docstring(target) or ""
                    symbols.append(relative + ":" + name)
                    if not doc:
                        failures.append(name + ": missing docstring")
                    if "Examples:" not in doc:
                        failures.append(name + ": missing example")
                    if isinstance(target, ast.FunctionDef):
                        required = ["Returns:"]
                        if "No exceptions are raised." not in doc:
                            required.append("Raises:")
                        params = [a.arg for a in target.args.posonlyargs + target.args.args + target.args.kwonlyargs
                                  if a.arg not in {"self", "cls"}]
                        if params or target.args.vararg or target.args.kwarg:
                            required.append("Args:")
                        for section in required:
                            if section not in doc:
                                failures.append(name + ": missing " + section)
    markers = []
    authored = [ROOT / "server.py", *sorted((ROOT / "samples").glob("*.py")),
                *sorted((ROOT / "tests").glob("*.py")), *sorted((ROOT / "scripts").glob("*.py"))]
    for path in authored:
        for token in tokenize.generate_tokens(io.StringIO(path.read_text(encoding="utf-8")).readline):
            if token.type == tokenize.COMMENT and re.search(r"\b(?:TODO|FIXME)\b", token.string):
                markers.append({"file": path.relative_to(ROOT).as_posix(), "line": token.start[0], "comment": token.string})
                if not re.search(r"(?:TODO|FIXME)\(#\d+\):", token.string):
                    failures.append("Untracked debt marker: " + str(markers[-1]))
    result = {"public_symbol_count": len(symbols), "public_symbols": symbols,
              "authored_python_files_scanned": len(authored), "debt_markers": markers,
              "failures": failures, "status": "passed" if not failures else "failed"}
    destination = ROOT / "evidence/sprint06/documentation-check.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())
