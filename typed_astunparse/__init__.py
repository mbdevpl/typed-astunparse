"""This is "__init__.py" file for "typed_astunparse" package.

functions: unparse, dump
"""

import ast
import typing as t

import typed_ast.ast3
from six.moves import cStringIO

from .unparser import Unparser
from .printer import Printer
from ._version import VERSION

__version__ = VERSION


def unparse(tree: t.Union[ast.AST, typed_ast.ast3.AST]) -> str:
    """Unparse the abstract syntax tree into a str.

    Behave just like astunparse.unparse(tree), but handle trees which are typed, untyped, or mixed.
    In other words, a mixture of ast.AST-based and typed_ast.ast3-based nodes will be unparsed.
    """
    stream = cStringIO()
    Unparser(tree, file=stream)
    return stream.getvalue()


def dump(
        tree: t.Union[ast.AST, typed_ast.ast3.AST], annotate_fields: bool = True,
        include_attributes: bool = False) -> str:
    """Behave just like astunparse.dump(tree), but handle typed_ast.ast3-based trees."""
    stream = cStringIO()
    Printer(
        file=stream, annotate_fields=annotate_fields,
        include_attributes=include_attributes).visit(tree)
    return stream.getvalue()


__all__ = ['unparse', 'dump']
