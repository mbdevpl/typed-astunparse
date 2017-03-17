# Copyright 2016-2017  Mateusz Bysiek  http://mbdev.pl/
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

"""Class: Printer."""

import ast
import sys

import astunparse
import typed_ast.ast3


class Printer(astunparse.Printer):

    """Partial rewrite of Printer from astunparse to handle typed_ast.ast3-based trees."""

    def __init__(
            self, file=sys.stdout, indent="  ", annotate_fields: bool=True,
            include_attributes: bool=False):
        """Initialize Printer instance."""
        super().__init__(file=file, indent=indent)
        self._annotate_fields = annotate_fields
        self._include_attributes = include_attributes

    def _prepare_for_print(self, node):
        if isinstance(node, list):
            nodestart = "["
            nodeend = "]"
            children = [("", child) for child in node]
        else:
            nodestart = type(node).__name__ + "("
            nodeend = ")"
            children = [
                (name + "=" if self._annotate_fields else '', value)
                for name, value in typed_ast.ast3.iter_fields(node)]
            if self._include_attributes and node._attributes:
                children += [
                    (attr + '=' if self._annotate_fields else '', getattr(node, attr))
                    for attr in node._attributes]

        return nodestart, children, nodeend

    def generic_visit(self, node):
        """Print the syntax tree without unparsing it.

        Merge of astunparse.Printer.generic_visit() and typed_ast.ast3.dump().
        """
        nodestart, children, nodeend = self._prepare_for_print(node)

        if len(children) > 1:
            self.indentation += 1

        self.write(nodestart)
        for i, pair in enumerate(children):
            attr, child = pair
            if len(children) > 1:
                self.write("\n" + self.indent_with * self.indentation)
            if isinstance(child, (ast.AST, typed_ast.ast3.AST, list)):
                self.write(attr)
                self.visit(child)
            else:
                self.write(attr + repr(child))

            if i != len(children) - 1:
                self.write(",")
        self.write(nodeend)

        if len(children) > 1:
            self.indentation -= 1
