# Sphinx configuration file

import os
import sys

# Add project root to Python path for autodoc
sys.path.insert(0, os.path.abspath(".."))

# -- Project information --
project = "pylsp-rope"
copyright = "2024, pylsp-rope contributors"
author = "pylsp-rope contributors"
release = "0.1.4"

# -- General configuration --
extensions = [
    "myst_parser",  # Markdown support
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
]

# MyST parser configuration
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "html_admonition",
    "linkify",
    "replacements",
    "smartquotes",
    "substitution",
    "tasklist",
]

# -- Options for HTML output --
html_theme = "sphinx_rtd_theme"
html_static_path = []
html_theme_options = {
    "canonical_url": "",
    "analytics_id": "",
    "logo_only": False,
    "prev_next_buttons_location": "bottom",
    "style_external_links": False,
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}

# -- Master document --
master_doc = "index"

# -- Exclude patterns --
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for other output formats --
htmlhelp_basename = "pylsp-ropedoc"
latex_documents = [
    (
        master_doc,
        "pylsp-rope.tex",
        "pylsp-rope Documentation",
        "pylsp-rope contributors",
        "manual",
    ),
]

man_pages = [(master_doc, "pylsp-rope", "pylsp-rope Documentation", [author], 1)]

texinfo_documents = [
    (
        master_doc,
        "pylsp-rope",
        "pylsp-rope Documentation",
        author,
        "pylsp-rope",
        "One line description of project.",
        "Miscellaneous",
    ),
]

# -- Exclude patterns --
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- ReadTheDocs specific configuration --
# When building on ReadTheDocs, these environment variables are available
if os.environ.get("READTHEDOCS") == "True":
    html_theme = "sphinx_rtd_theme"
