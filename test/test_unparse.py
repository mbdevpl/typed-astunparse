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

"""tested function: unparse"""

import logging
import unittest

import typed_ast.ast35
import typed_astunparse

from .examples import MODES, EXAMPLES, INVALID_EXAMPLES

_LOG = logging.getLogger(__name__)


class UnparseTests(unittest.TestCase):

    """Unit tests for unparse() function."""

    def test_unparse_examples(self):
        """Are ASTs of examples unparsed correctly?"""
        for description, example in EXAMPLES.items():
            for mode in MODES:
                if example['trees'][mode] is None:
                    continue
                code = typed_astunparse.unparse(example['trees'][mode])
                _LOG.debug('%s', code)
                code = code.strip()#replace('\n', '')
                self.assertEqual(code, example['code'], msg=(description, mode))

    def test_unparse_invalid_examples(self):
        """Are ASTs of invalid examples raising errors as expected?"""
        for description, example in INVALID_EXAMPLES.items():
            for mode in MODES:
                if example['trees'][mode] is None:
                    continue
                with self.assertRaises(SyntaxError, msg=(description, mode)) as raised:
                    _ = typed_astunparse.unparse(example['trees'][mode])
                self.assertIn('PEP 526', str(raised.exception), msg=(description, mode))

                with self.assertRaises(SyntaxError, msg=(description, mode)):# as raised:
                    _ = typed_ast.ast35.parse(source=example['code'], mode=mode)
                #self.assertIn('invalid syntax', str(raised.exception), msg=(description, mode))

    def test_many_roundtrips(self):
        """Are ASTs preserved when doing parse(unparse(parse(...unparse(parse(code))...)))?"""
        for description, example in EXAMPLES.items():
            for mode in MODES:
                if example['trees'][mode] is None:
                    continue

                tree = example['trees'][mode]
                for _ in range(10):
                    code = typed_astunparse.unparse(tree)
                    _LOG.debug('%s', code)
                    clean_code = code.strip()
                    self.assertEqual(clean_code, example['code'], msg=(description, mode))
                    tree = typed_ast.ast35.parse(source=code, mode=mode)
