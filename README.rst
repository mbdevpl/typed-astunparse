
================
typed-astunparse
================

.. image:: https://img.shields.io/pypi/v/typed-astunparse.svg
    :target: https://pypi.python.org/pypi/typed-astunparse
    :alt: package version from PyPI

.. image:: https://travis-ci.org/mbdevpl/typed-astunparse.svg?branch=master
    :target: https://travis-ci.org/mbdevpl/typed-astunparse
    :alt: build status from Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/github/mbdevpl/typed-astunparse?svg=true
    :target: https://ci.appveyor.com/project/mbdevpl/typed-astunparse
    :alt: build status from AppVeyor

.. image:: https://coveralls.io/repos/github/mbdevpl/typed-astunparse/badge.svg?branch=master
    :target: https://coveralls.io/github/mbdevpl/typed-astunparse?branch=master
    :alt: test coverage from Coveralls

.. image:: https://landscape.io/github/mbdevpl/typed-astunparse/master/landscape.svg?style=flat
    :target: https://landscape.io/github/mbdevpl/typed-astunparse/master
    :alt: code health from Landscape

.. image:: https://codeclimate.com/github/mbdevpl/typed-astunparse/badges/gpa.svg
    :target: https://codeclimate.com/github/mbdevpl/typed-astunparse
    :alt: code GPA from Code Climate

.. image:: https://codeclimate.com/github/mbdevpl/typed-astunparse/badges/issue_count.svg
    :target: https://codeclimate.com/github/mbdevpl/typed-astunparse
    :alt: issue count from Code Climate

.. image:: https://img.shields.io/pypi/l/typed-astunparse.svg
    :alt: license

.. role:: bash(code)
    :language: bash

.. role:: python(code)
    :language: python

The *typed-astunparse* is to *typed-ast* as *astunparse* is to *ast*. In short: unparsing of Python
3 abstract syntax trees (AST) with type comments.

The built-in *ast* module can parse Python source code into AST. It can't, however, generate source
code from the AST. That's where *astunparse* comes in. Using a refactored version of an obscure
script found in official Python repository, it provides code generation capability for native
Python AST.

The *ast* and *astunparse* modules, however, completely ignore type comments introduced in
PEP 484. They treat them like all other comments, so when you parse the code using
:python:`compile()`, your type comments will be lost. There is no place for them in the AST, so
obviously they also cannot be unparsed.

The *typed-ast* module provides an updated AST including type comments defined in PEP 484 and
a parser for Python code that contains such comments.

Unfortunately, *typed-ast* doesn't provide any means to go from AST back to source code with type
comments. This is where this module, *typed-astunparse*, comes in. It provides unparser for AST
defined in *typed-ast*.


------------
requirements
------------

This package is intended for Python 3.3 and later. It is tested on Linux (Travis CI)
and Windows (AppVeyor), but it might work on other systems too.

*typed-astunparse* mainly depends on:

-  *astunparse*

-  *typed-ast*


------------
installation
------------

For simplest installation use :bash:`pip`:

.. code:: bash

    pip install typed-astunparse

You can also build your own version:

.. code:: bash

    git clone https://github.com/mbdevpl/typed-astunparse
    cd typed-astunparse
    python -m unittest discover # make sure the tests pass
    python setup.py bdist_wheel
    ls -1tr dist/*.whl | tail -n 1 | xargs pip install


-----
usage
-----

Example of roundtrip from code through AST to code:

.. code:: python

    import typed_ast.ast3
    import typed_astunparse

    code = 'my_string = None # type: str'
    roundtrip = typed_astunparse.unparse(typed_ast.ast3.parse(code))
    print(roundtrip)

for more examples see :bash:`examples.ipynb` notebook.


-----
links
-----

-  *ast*:

   https://docs.python.org/3/library/ast.html

   https://greentreesnakes.readthedocs.io/

-  *astunparse*:

   https://pypi.python.org/pypi/astunparse

   https://github.com/simonpercivall/astunparse

   https://astunparse.readthedocs.io/en/latest/

-  PEP 483 - The Theory of Type Hints:

   https://www.python.org/dev/peps/pep-0483/

-  PEP 484 - Type Hints:

   https://www.python.org/dev/peps/pep-0484/

-  PEP 3107 - Function Annotations:

   https://www.python.org/dev/peps/pep-3107/

-  PEP 526 - Syntax for Variable Annotations:

   https://www.python.org/dev/peps/pep-0526/

-  *typed-ast*:

   https://pypi.python.org/pypi/typed-ast

   https://github.com/python/typed_ast
