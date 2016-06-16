
================
typed_astunparse
================

.. image:: https://badge.fury.io/py/typed-astunparse.svg
    :target: https://badge.fury.io/py/typed-astunparse

.. image:: https://travis-ci.org/mbdevpl/typed-astunparse.svg?branch=master
    :target: https://travis-ci.org/mbdevpl/typed-astunparse

What *astunparse* is for *ast*, *typed-astunparse* is for *typed-ast*.

The built-in *ast* module has capabilites to parse Python source code into abstract syntax tree
(AST). It does not, however, have neiter capability to go back from AST to source code nor
capability to print the AST in human-readable format.

That's where *astunparse* comes in. It provides those capabilites.

Built-in *ast* module, however, completely ignores type comments introduced in PEP 484. It treats
them like all other comments. The *typed-ast* module has capabilites to parse Python source code
into abstract syntax tree (AST), including type comments defined in PEP 484.

Unfortunately, *typed-ast* also doesn't provide any means to go from AST to source code. This is
where *typed-astunparse* comes in. It provides unparser for AST defined in *typed-ast*.

------------
requirements
------------

This package is intendended for Python 3.5 and above. It was tested on 64 bit Ubuntu,
but it might work on other versions and systems too.

typed-astunparse depends on:

-  astunparse

-  typed-ast

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

-  PEP 484:

   https://www.python.org/dev/peps/pep-0484/

-  *typed-ast*:

   https://pypi.python.org/pypi/typed-ast

   https://github.com/dropbox/typed_ast
