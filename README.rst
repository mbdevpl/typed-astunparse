.. role:: bash(code)
    :language: bash

.. role:: python(code)
    :language: python


================
typed-astunparse
================

.. image:: https://img.shields.io/pypi/v/typed-astunparse.svg
    :target: https://pypi.org/project/typed-astunparse
    :alt: package version from PyPI

.. image:: https://travis-ci.org/mbdevpl/typed-astunparse.svg?branch=master
    :target: https://travis-ci.org/mbdevpl/typed-astunparse
    :alt: build status from Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/github/mbdevpl/typed-astunparse?svg=true
    :target: https://ci.appveyor.com/project/mbdevpl/typed-astunparse
    :alt: build status from AppVeyor

.. image:: https://api.codacy.com/project/badge/Grade/4a6d141d87c346f0b3c0d50d76a10e32
    :target: https://www.codacy.com/app/mbdevpl/typed-astunparse
    :alt: grade from Codacy

.. image:: https://codecov.io/gh/mbdevpl/typed-astunparse/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/mbdevpl/typed-astunparse
    :alt: test coverage from Codecov

.. image:: https://img.shields.io/pypi/l/typed-astunparse.svg
    :target: https://github.com/mbdevpl/typed-astunparse/blob/master/NOTICE
    :alt: license

The *typed-astunparse* is to *typed-ast* as *astunparse* is to *ast*. In short: unparsing of Python
3 abstract syntax trees (AST) with type comments.

.. contents::
    :backlinks: none


Why this module was created
===========================

The built-in *ast* module can parse Python source code into AST but it can't generate source
code from the AST. The *astunparse* module (using a refactored version of an obscure
script found in official Python repository) provides code generation capability for native
Python AST.

However, both *ast* and *astunparse* modules completely ignore type comments introduced in
PEP 484. They treat them like all other comments, so when you parse the code using
:python:`compile()`, your type comments will be lost. There is no place for them in the AST, so
obviously they also cannot be unparsed.

The *typed-ast* module provides an updated AST including type comments defined in PEP 484 and
a parser for Python code that contains such comments.

Unfortunately, *typed-ast* doesn't provide any means to go from AST back to source code with type
comments. This is why module *typed-astunparse* (i.e. this one) was created: to provide unparser
for AST defined in *typed-ast*.


Usage
=====

Example of roundtrip from code through AST to code:

.. code:: python

    import typed_ast.ast3
    import typed_astunparse

    code = 'my_string = None  # type: str'
    roundtrip = typed_astunparse.unparse(typed_ast.ast3.parse(code))
    print(roundtrip)

This will print:

.. code:: python

    my_string = None  # type: str


for more examples see `<examples.ipynb>`_ notebook.



Installation
============

For simplest installation use :bash:`pip`:

.. code:: bash

    pip3 install typed-astunparse

You can also build your own version:

.. code:: bash

    git clone https://github.com/mbdevpl/typed-astunparse
    cd typed-astunparse
    pip3 install -U test_requirements.txt
    python3 -m unittest  # make sure the tests pass
    python3 setup.py bdist_wheel
    pip3 install dist/*.whl


Requirements
------------

Python version 3.5 or later.

Python libraries as specified in `<requirements.txt>`_.

Building and running tests additionally requires packages listed in `<test_requirements.txt>`_.

Tested on Linux, OS X and Windows.


Links
=====


Extensions of this module
-------------------------

If you're extending typed-astunparse and you'd like to share why,
feel free to submit a `pull request <https://github.com/mbdevpl/typed-astunparse/pulls>`_
introducing your project.

-   *horast*: human-oriented ast

    Built upon both *typed-ast* and *typed-astunparse* providing parsing and unparsing
    of arbitrary comments in addition to type comments.

    https://pypi.org/project/horast

    https://github.com/mbdevpl/horast


Who's using this module and why
-------------------------------

If you're using typed-astunparse in your work and you'd like to share why,
feel free to submit a `pull request <https://github.com/mbdevpl/typed-astunparse/pulls>`_
introducing your project.

-   *static-typing*: using *typed-astunparse* directly to provide AST unparsing function

    https://pypi.org/project/static-typing

    https://github.com/mbdevpl/static-typing


References
----------

-   *ast*:

    https://docs.python.org/3/library/ast.html

    https://greentreesnakes.readthedocs.io/

-   *astunparse*:

    https://pypi.org/project/astunparse

    https://github.com/simonpercivall/astunparse

    https://astunparse.readthedocs.io/en/latest/

-   PEP 483 - The Theory of Type Hints:

    https://www.python.org/dev/peps/pep-0483/

-   PEP 484 - Type Hints:

    https://www.python.org/dev/peps/pep-0484/

-   PEP 3107 - Function Annotations:

    https://www.python.org/dev/peps/pep-3107/

-   PEP 526 - Syntax for Variable Annotations:

    https://www.python.org/dev/peps/pep-0526/

-   *typed-ast*:

    https://pypi.org/project/typed-ast

    https://github.com/python/typed_ast
