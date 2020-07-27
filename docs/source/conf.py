# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import django
import os
import sys


sys.path.insert(0, os.path.abspath("../../"))
os.environ["DJANGO_SETTINGS_MODULE"] = "tests.test_settings"
django.setup()

# -- Project information -----------------------------------------------------

project = "django_mri"
copyright = "2020, Zvi Baratz"
author = "Zvi Baratz"

# The full version, including alpha/beta/rc tags
release = "0.1.0"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.coverage",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
]

EXLUDED_MEMBERS = (
    # Default Django fields, methods, and exceptions that are created in
    # models but do not require documentation.
    # Fields
    "added_by_id",
    "dicom_id",
    "definition_id",
    "id",
    "input_ptr",
    "input_ptr_id",
    "inputdefinition_ptr",
    "inputdefinition_ptr_id",
    "outputdefinition_ptr",
    "outputdefinition_ptr_id",
    "output_ptr",
    "output_ptr_id",
    "subject_id",
    "value_id",
    # Methods
    "get_next_by_created",
    "get_next_by_modified",
    "get_previous_by_created",
    "get_previous_by_modified",
    # Exceptions
    "DoesNotExist",
    "MultipleObjectsReturned",
    # Other
    "Meta",
)

autodoc_default_options = {
    "exclude-members": ", ".join(EXLUDED_MEMBERS),
    "undoc-members": False,
    "member-order": "groupwise",
}

# Allow safely referencing sections between documents.
# See:
# https://www.sphinx-doc.org/en/master/usage/extensions/autosectionlabel.html#confval-autosectionlabel_prefix_document
autosectionlabel_prefix_document = True

# Intersphinx
intersphinx_mapping = {
    "django": ("http://django.readthedocs.org/en/latest/", None),
    "django_analyses": (
        "http://django_analyses.readthedocs.org/en/latest/",
        None,
    ),
    "django_dicom": ("http://django_dicom.readthedocs.org/en/latest/", None),
    "django_filters": (
        "https://django-filter.readthedocs.io/en/master/",
        None,
    ),
    "nipype": ("http://nipype.readthedocs.org/en/latest/", None),
    "python": ("https://docs.python.org/3", None),
}


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

# Sphinx expects the master file to be "contents.rst"
# Fix based on
# https://stackoverflow.com/questions/56336234/build-fail-sphinx-error-contents-rst-not-found
master_doc = "index"
