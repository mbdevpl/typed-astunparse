
================
typed-astunparse
================

.. image:: https://badge.fury.io/py/typed-astunparse.svg
    :target: https://badge.fury.io/py/typed-astunparse

.. image:: https://travis-ci.org/mbdevpl/typed-astunparse.svg?branch=master
    :target: https://travis-ci.org/mbdevpl/typed-astunparse

.. role:: bash(code)
   :language: bash

.. role:: python(code)
   :language: python

The *typed-astunparse* is to *typed-ast* as *astunparse* is to *ast*. In short: unparsing of Python
3.5 abstract syntax trees (AST) with type comments.

The built-in *ast* module has capabilites to parse Python source code into AST. It does not,
however, have the capability to generate source code from the AST. That's where *astunparse* comes
in. Using a refactored version of an obscure script found in official Python repository, it provides
code generation capability for built-in AST.

Built-in *ast* module, however, completely ignores type comments introduced in PEP 484. It treats
them like all other comments, so when you parse the code using :python:`compile()`, your type
comments will be lost. The *typed-ast* module intoduces AST and parser that includes type comments
defined in PEP 484.

Unfortunately, *typed-ast* also doesn't provide any means to go from AST to source code. This is
where this module, *typed-astunparse*, comes in. It provides unparser for AST defined in
*typed-ast*.

------------
requirements
------------

This package is intendended for Python 3.5. It was tested on 64 bit Ubuntu, but it might work on
other versions and systems too.

typed-astunparse depends on:

-  astunparse

-  typed-ast

------------
installation
------------

For simplest installation use :bash:`pip`:

.. code:: bash

    pip3.5 install typed-astunparse

You can also build your own version:

.. code:: bash

    git clone
    cd typed-astunparse
    python3.5 -m unittest discover # make sure the tests pass
    python3.5 setup.py bdsit_wheel
    find dist -name "typed_astunparse-*" | tail -n 1 | xargs pip3.5 install

-----
usage
-----

Example of roundtrip from code through AST to code:

.. code:: python

    import typed_ast
    import typed_astunparse

    code = 'my_string = None # type: str'
    roundtrip = typed_astunparse.unparse(typed_ast.parse(code))
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

-  PEP 484:

   https://www.python.org/dev/peps/pep-0484/

-  *typed-ast*:

   https://pypi.python.org/pypi/typed-ast

   https://github.com/dropbox/typed_ast
