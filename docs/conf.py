author = "Akio Taniguchi"
copyright = "2026 Akio Taniguchi"
project = "Readonlydict"
release = version = "1.0.0rc1"

autodoc_default_options = {
    "inherited-members": True,
    "special-members": True,
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
