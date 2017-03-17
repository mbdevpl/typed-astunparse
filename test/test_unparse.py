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

"""Tested function: unparse."""

import ast
import logging
import unittest

import typed_ast.ast3
import typed_astunparse

from .examples import MODES, EXAMPLES, INVALID_EXAMPLES, PATHS

_LOG = logging.getLogger(__name__)


class UnparseTests(unittest.TestCase):

    """Unit tests for unparse() function."""

    def test_unparse_examples(self):
        """Unparse ASTs of examples correctly."""
        for description, example in EXAMPLES.items():
            for mode in MODES:
                if example['trees'][mode] is None:
                    continue
                code = typed_astunparse.unparse(example['trees'][mode])
                _LOG.debug('%s', code)
                code = code.strip()
                self.assertEqual(code, example['code'], msg=(description, mode))

    def test_unparse_invalid_examples(self):
        """Raise errors on ASTs of invalid examples as expected."""
        for description, example in INVALID_EXAMPLES.items():
            for mode in MODES:
                if example['trees'][mode] is None:
                    continue
                with self.assertRaises(SyntaxError, msg=(description, mode)) as raised:
                    typed_astunparse.unparse(example['trees'][mode])
                self.assertIn('PEP 526', str(raised.exception), msg=(description, mode))

                with self.assertRaises(SyntaxError, msg=(description, mode)):
                    typed_ast.ast3.parse(source=example['code'], mode=mode)

    def test_many_roundtrips(self):
        """Prserve ASTs when doing parse(unparse(parse(...unparse(parse(code))...)))."""
        for description, example in EXAMPLES.items():
            for mode in MODES:
                if example['trees'][mode] is None:
                    continue

                tree = example['trees'][mode]
                for _ in range(4):
                    code = typed_astunparse.unparse(tree)
                    _LOG.debug('%s', code)
                    clean_code = code.strip()
                    self.assertEqual(clean_code, example['code'], msg=(description, mode))
                    tree = typed_ast.ast3.parse(source=code, mode=mode)

    def test_files(self):
        """Keep Python stdlib tree the same after roundtrip parse-unparse."""
        for path in PATHS:
            with open(path, 'r', encoding='utf-8') as py_file:
                original_code = py_file.read()
            tree = typed_ast.ast3.parse(source=original_code, filename=path)
            code = typed_astunparse.unparse(tree)
            try:
                roundtrip_tree = typed_ast.ast3.parse(source=code)
            except SyntaxError as err:
                self.fail(msg='bad syntax after unparsing "{}"\n{}'.format(path, err))
            tree_dump = typed_ast.ast3.dump(tree, include_attributes=False)
            roundtrip_tree_dump = typed_ast.ast3.dump(roundtrip_tree, include_attributes=False)
            self.assertEqual(tree_dump, roundtrip_tree_dump, msg=path)

    def test_untyped_files(self):
        """Unparse Python stdlib correctly even if parsed using built-in ast package."""
        for path in PATHS:
            with open(path, 'r', encoding='utf-8') as py_file:
                original_code = py_file.read()
            tree = ast.parse(source=original_code, filename=path)
            code = typed_astunparse.unparse(tree)
            roundtrip_tree = ast.parse(source=code)
            tree_dump = ast.dump(tree, include_attributes=False)
            roundtrip_tree_dump = ast.dump(roundtrip_tree, include_attributes=False)
            self.assertEqual(tree_dump, roundtrip_tree_dump, msg=path)
