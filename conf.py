"""Build configuration; an internal documentation tool, not an application API."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "samples"))
project = "Personal Assistant API | Sprint 06"
author = "P. Dulguun | 23B1NUM1041"
copyright = "2026, P. Dulguun"
release = "6.0"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx.ext.doctest", "sphinx.ext.viewcode", "sphinx.ext.intersphinx"]
intersphinx_mapping = {"python": ("https://docs.python.org/3.12", str(Path(__file__).parent / "_inventories/python.inv"))}
autodoc_member_order = "bysource"
autoclass_content = "both"
autodoc_typehints = "description"
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_use_param = False
napoleon_use_rtype = False
html_theme = "alabaster"
html_theme_options = {"description": "Structured docstrings, verified examples, and an evidence-based AI audit.", "fixed_sidebar": True, "sidebar_width": "250px", "page_width": "1100px"}
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_title = "Sprint 06 - Personal Assistant API"
exclude_patterns = ["_inventories/**"]
doctest_global_setup = "import sys\nfrom pathlib import Path\nimport server\nimport client\nfrom server import *\nfrom client import *\n"
# The API documents standard-library exceptions as literal types in Google sections.
# Application cross-references are checked with -n; no blanket warning suppression.
nitpick_ignore = []
