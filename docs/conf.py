author = "Akio Taniguchi"
copyright = "2026 Akio Taniguchi"
project = "ReadonlyDict"
release = version = "2.0.0"

autodoc_default_options = {
    "inherited-members": True,
    "special-members": (
        "__getitem__,"
        "__hash__,"
        "__init__,"
        "__iter__,"
        "__len__,"
        "__or__,"
        "__ror__,"
        "__repr__,"
        "__reversed__"
    ),
    "undoc-members": True,
}
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]
html_static_path = ["_static"]
html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "github_url": "https://github.com/astropenguin/readonlydict",
    "logo": {"text": project},
    "navbar_end": [
        "version-switcher",
        "theme-switcher",
        "navbar-icon-links",
    ],
    "switcher": {
        "json_url": "https://astropenguin.github.io/readonlydict/_static/switcher.json",
        "version_match": version,
    },
}
