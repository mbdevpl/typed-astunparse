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
import typed_ast.ast35

class Unparser(astunparse.Unparser):
    """ Partial rewrite of Unparser from astunparse to handle typed_ast.ast35-based trees. """

    # TODO: for most nodes still using default unparser that ignores type comments

    def write_type_comment(self, type_comment):
        self.write(" # type: ")
        if isinstance(type_comment, str):
            self.write(type_comment)
        else:
            self.dispatch(type_comment)

    def _Assign(self, t):
        super()._Assign(t)
        if t.type_comment:
            self.write_type_comment(t.type_comment)
