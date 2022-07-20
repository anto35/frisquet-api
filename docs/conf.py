"""Sphinx configuration."""
project = "Frisquet Api"
author = "anto35"
copyright = "2022, anto35"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
