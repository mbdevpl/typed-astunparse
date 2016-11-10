# Copyright 2016  Mateusz Bysiek  http://mbdev.pl/
# This file is part of typed-astunparse.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This is "__init__.py" file for "typed_astunparse" package.

functions: unparse, dump
"""

from __future__ import absolute_import

import typed_ast.ast35
from six.moves import cStringIO

from .unparser import Unparser
from .printer import Printer
from ._version import VERSION

__version__ = VERSION


def unparse(tree: typed_ast.ast35.AST):
    """Behave just like astunparse.unparse(tree), but handle typed_ast.ast35-based trees."""
    stream = cStringIO()
    Unparser(tree, file=stream)
    return stream.getvalue()


def dump(tree: typed_ast.ast35.AST):
    """Behave just like astunparse.dump(tree), but handle typed_ast.ast35-based trees."""
    stream = cStringIO()
    Printer(file=stream).visit(tree)
    return stream.getvalue()

__all__ = ['unparse', 'dump']
