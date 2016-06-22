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

"""
class: Unparser
"""

import astunparse
from astunparse.unparser import interleave
import typed_ast.ast35

class Unparser(astunparse.Unparser):
    """ Partial rewrite of Unparser from astunparse to handle typed_ast.ast35-based trees. """

    boolops = {**astunparse.Unparser.boolops, typed_ast.ast35.And: 'and', typed_ast.ast35.Or: 'or'}
    """ Mapping from boolean operation node to its string representation.

    This overrides of base class dict, because {ast.And: 'and', ast.Or: 'or'} obviously causes
    errors.
    """

    def _write_string_or_dispatch(self, t):
        """ If t is str, write it. Otherwise, dispatch it. """

        if isinstance(t, str):
            self.write(t)
        else:
            self.dispatch(t)

    def _fill_type_comment(self, type_comment):
        """ Unparse type comment, adding it on the next line. """

        self.fill("# type: ")
        self._write_string_or_dispatch(type_comment)

    def _write_type_comment(self, type_comment):
        """ Unparse type comment, appending it to the end of the current line. """

        self.write(" # type: ")
        self._write_string_or_dispatch(type_comment)

    def _generic_FunctionDef(self, t, async=False):
        """ Unparse FunctionDef node.

        Rather than handling:

        FunctionDef(identifier name, arguments args,
                    stmt* body, expr* decorator_list, expr? returns)

        handle:

        FunctionDef(identifier name, arguments args,
                    stmt* body, expr* decorator_list, expr? returns, string? type_comment)
        """

        if t.type_comment is None:
            super()._generic_FunctionDef(t)
            return

        self.write("\n")
        for deco in t.decorator_list:
            self.fill("@")
            self.dispatch(deco)
        self.fill(("async " if async else "") + "def " + t.name + "(")
        self.dispatch(t.args)
        self.write(")")
        if getattr(t, "returns", False):
            self.write(" -> ")
            self.dispatch(t.returns)
        self.enter()
        self._fill_type_comment(t.type_comment)
        self.dispatch(t.body)
        self.leave()

    def _Assign(self, t):
        """ Unparse Assign node.

        Rather than handling just:

        Assign(expr* targets, expr value)

        handle:

        Assign(expr* targets, expr value, string? type_comment)
        """

        super()._Assign(t)

        if t.type_comment is not None:
            self._write_type_comment(t.type_comment)

    def _For(self, t):
        """ Unparse For node.

        Rather than handling just:

        For(expr target, expr iter, stmt* body, stmt* orelse)

        handle:

        For(expr target, expr iter, stmt* body, stmt* orelse, string? type_comment)
        """

        if t.type_comment is None:
            super()._For(t)
            return

        self.fill("for ")
        self.dispatch(t.target)
        self.write(" in ")
        self.dispatch(t.iter)
        self.enter()
        self._write_type_comment(t.type_comment)
        self.dispatch(t.body)
        self.leave()
        if t.orelse:
            self.fill("else")
            self.enter()
            self.dispatch(t.orelse)
            self.leave()

    def _With(self, t):
        """ Unparse With node.

        Rather than handling just:

        For(expr target, expr iter, stmt* body, stmt* orelse)

        handle:

        For(expr target, expr iter, stmt* body, stmt* orelse, string? type_comment)
        """

        if t.type_comment is None:
            super()._With(t)
            return

        self.fill("with ")
        if hasattr(t, 'items'):
            interleave(lambda: self.write(", "), self.dispatch, t.items)
        else:
            self.dispatch(t.context_expr)
            if t.optional_vars:
                self.write(" as ")
                self.dispatch(t.optional_vars)
        self.enter()
        self._write_type_comment(t.type_comment)
        self.dispatch(t.body)
        self.leave()
