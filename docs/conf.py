from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "nerva-py"
author = "Sayan Bhattacharyya"
copyright = f"2024, {author}"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
]

html_theme = "furo"

autodoc_member_order = "bysource"
autodoc_typehints = "description"
napoleon_numpy_docstring = True
napoleon_google_docstring = False
suppress_warnings = ["ref.duplicate"]
