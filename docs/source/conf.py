# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'hPIC2'
copyright = '2023, hPIC2'
author = 'lcpp'

release = '0.1'
version = '0.1.0'

# -- General configuration

numfig = True

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinxcontrib.bibtex',
    'sphinxcontrib.pseudocode',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.intersphinx'
]

bibtex_bibfiles = ['refs.bib']

autosectionlabel_prefix_document = True

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'

html_last_updated_fmt = ""

html_context = {
"display_github": False, # Add 'Edit on Github' link instead of 'View page source'
"commit": False,
}

