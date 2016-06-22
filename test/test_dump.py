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

import typed_astunparse

from .examples import MODES as modes, EXAMPLES as examples

_LOG = logging.getLogger(__name__)

class DumpTests(unittest.TestCase):
    """ Unit tests for dump() function. """

    def test_dump_examples(self):
        """ Are ASTs of examples printed correctly? """

        for description, example in examples.items():
            for mode in modes:
                if example['trees'][mode] is None:
                    continue
                dump = typed_astunparse.dump(example['trees'][mode])
                _LOG.debug('%s', dump)
                dump = dump.replace('\n', '').replace(' ', '')
                self.assertEqual(dump, example['dumps'][mode], msg=(description, mode))
