# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

sys.path.insert(0, os.path.abspath('../..'))

project = 'Birthday Database'
copyright = '2024, Katzenkralle, DerVogel101'
author = 'Katzenkralle, DerVogel101'
release = '1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
        'sphinx.ext.autodoc',
        'sphinx.ext.todo',
        'sphinx.ext.viewcode',
        'sphinx.ext.napoleon',
        'sphinx.ext.autosummary',
        'sphinx.ext.autodoc.typehints'
]

templates_path = ['_templates']
exclude_patterns = [".vscode", "__pycache__"]

autodoc_default_options = {
    'undoc-members': True,
    'private-members': True,
}

# Include TODOs in the generated documentation
todo_include_todos = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Add the custom CSS file
html_css_files = [
    'custom.css',
]