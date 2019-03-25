"""Tested function: unparse."""

import ast
import itertools
import logging
import pathlib
import unittest
import sys

import typed_ast.ast3
import typed_astunparse

from .examples import MODES, EXAMPLES, UNVERIFIED_EXAMPLES, INVALID_EXAMPLES, PATHS

_LOG = logging.getLogger(__name__)


class UnparseTests(unittest.TestCase):

    """Unit tests for unparse() function."""

    maxDiff = None

    def test_unparse_examples(self):
        """Unparse ASTs of examples correctly."""
        for description, example in itertools.chain(EXAMPLES.items(), UNVERIFIED_EXAMPLES.items()):
            for mode in MODES:
                if example['trees'][mode] is None:
                    continue
                with self.subTest(description=description):
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
                with self.assertRaises(SyntaxError, msg=(description, mode)):
                    typed_ast.ast3.parse(source=example['code'], mode=mode)

                code = typed_astunparse.unparse(example['trees'][mode])
                tree = None
                try:
                    tree = typed_ast.ast3.parse(source=code, mode=mode)
                except SyntaxError:
                    continue
                code = typed_astunparse.unparse(tree)

    def test_bad_raw_literal(self):
        raw_literal = rb'''\t\t ' """ ''' + rb""" " ''' \n"""
        tree = typed_ast.ast3.Bytes(raw_literal, 'rb')
        code = typed_astunparse.unparse(tree)
        _LOG.debug('%s', code)
        self.assertNotEqual(raw_literal, code)
        for mode in MODES:
            tree = typed_ast.ast3.parse(source=code, mode=mode)

    def test_many_roundtrips(self):
        """Prserve ASTs when doing parse(unparse(parse(...unparse(parse(code))...)))."""
        for description, example in EXAMPLES.items():
            for mode in MODES:
                if example['trees'][mode] is None:
                    continue

                tree = example['trees'][mode]
                with self.subTest(description=description):
                    for _ in range(4):
                        code = typed_astunparse.unparse(tree)
                        _LOG.debug('%s', code)
                        clean_code = code.strip()
                        self.assertEqual(clean_code, example['code'], msg=(description, mode))
                        tree = typed_ast.ast3.parse(source=code, mode=mode)

    def test_files(self):
        """Keep Python stdlib tree the same after roundtrip parse-unparse."""
        for path in PATHS:
            if sys.version_info[:2] == (3, 7) and pathlib.Path(path).name == 'dataclasses.py':
                continue
            with open(path, 'r', encoding='utf-8') as py_file:
                original_code = py_file.read()
            tree = typed_ast.ast3.parse(source=original_code, filename=path)
            code = typed_astunparse.unparse(tree)
            with self.subTest(path=path):
                roundtrip_tree = typed_ast.ast3.parse(source=code)
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
            with self.subTest(path=path):
                roundtrip_tree = ast.parse(source=code)
                tree_dump = ast.dump(tree, include_attributes=False)
                roundtrip_tree_dump = ast.dump(roundtrip_tree, include_attributes=False)
                self.assertEqual(tree_dump, roundtrip_tree_dump, msg=path)
