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
tested function: dump
"""

import logging
import unittest

import typed_ast.ast35
import typed_astunparse

_LOG = logging.getLogger(__name__)

class DumpTests(unittest.TestCase):
    """ Unit tests for dump() function. """

    def test_addition(self):
        """ Is AST of "a + b" printed correctly? """

        tree = typed_ast.ast35.BinOp(
            typed_ast.ast35.Name('a', typed_ast.ast35.Load()), typed_ast.ast35.Add(),
            typed_ast.ast35.Name('b', typed_ast.ast35.Load()))

        tree_str = typed_astunparse.dump(tree)

        _LOG.debug('%s', tree_str)
        self.assertEqual(
            tree_str.replace('\n', '').replace(' ', ''),
            "BinOp(left=Name(id='a',ctx=Load()),op=Add(),right=Name(id='b',ctx=Load()))")
