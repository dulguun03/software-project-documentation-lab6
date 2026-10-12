"""Internal reflection checks for draft and corrected documentation symbols."""
import ast
import builtins
import importlib
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import server


def missing_references(text):
    """Inspect Handler method references; internal test helper, not public API."""
    names = set(re.findall(r"(?:self|Handler)\.([a-zA-Z_]\w*)\s*\(", text))
    return sorted(name for name in names if not callable(getattr(server.Handler, name, None)))


class HallucinationTests(unittest.TestCase):
    """Keep real draft checks separate from a deliberately seeded ghost API."""

    def test_declared_ai_methods_exist(self):
        tree = ast.parse((ROOT / "audit/ai_docstring.py").read_text(encoding="utf-8"))
        cls = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "Handler")
        for method in cls.body:
            if isinstance(method, ast.FunctionDef):
                self.assertTrue(callable(getattr(server.Handler, method.name, None)), method.name)

    def test_ai_and_corrected_method_references_exist(self):
        for relative in ["audit/ai_docstring.py", "manual_docstring.py"]:
            with self.subTest(file=relative):
                self.assertEqual(missing_references((ROOT / relative).read_text(encoding="utf-8")), [])

    def test_documented_exception_types_exist(self):
        for relative in ["audit/ai_docstring.py", "manual_docstring.py"]:
            tree = ast.parse((ROOT / relative).read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if not isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                    continue
                doc = ast.get_docstring(node) or ""
                for section in re.findall(r"Raises:\n(.*?)(?=\n\S|\Z)", doc, re.S):
                    for name in re.findall(r"^\s{4}([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*):", section, re.M):
                        if name == "None":
                            continue
                        if "." in name:
                            module, symbol = name.rsplit(".", 1)
                            actual = getattr(importlib.import_module(module), symbol, None)
                        else:
                            actual = getattr(server, name, getattr(builtins, name, None))
                        self.assertIsInstance(actual, type, name)
                        self.assertTrue(issubclass(actual, BaseException), name)

    def test_seeded_ghost_method_is_detected(self):
        text = (ROOT / "audit/negative_control_docstring.txt").read_text(encoding="utf-8")
        self.assertEqual(missing_references(text), ["cancel_action"])

    def test_invented_ai_request_fields_are_rejected(self):
        # Reflection cannot prove behavior; this assertion checks the invented schema.
        with self.assertRaises(server.RequestError) as caught:
            server.fields({"action": "confirmation", "session_id": "session_anu_01", "confirmed": True},
                          ["session_id", "payload_version"])
        self.assertEqual(caught.exception.status, 400)


if __name__ == "__main__":
    unittest.main()
