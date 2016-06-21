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
Examples used in unit tests.
"""

import typed_ast.ast35
import typed_astunparse

MODES = ['exec', 'eval', 'single']

EXAMPLES = {
    'addition': {
        'code': "(a + b)",
        'is_expression': True,
        'tree': typed_ast.ast35.BinOp(
            typed_ast.ast35.Name('a', typed_ast.ast35.Load()), typed_ast.ast35.Add(),
            typed_ast.ast35.Name('b', typed_ast.ast35.Load())),
        'dump': "BinOp(left=Name(id='a',ctx=Load()),op=Add(),right=Name(id='b',ctx=Load()))"
        },
    'type comment': {
        'code': "my_string = None # type: str",
        'is_expression': False,
        'tree': typed_ast.ast35.Assign(
            [typed_ast.ast35.Name('my_string', typed_ast.ast35.Store())],
            typed_ast.ast35.NameConstant(None),
            'str'),
        'dump': \
            "Assign(targets=[Name(id='my_string',ctx=Store())],value=NameConstant(value=None)," \
            "type_comment='str')"
        },
    'type annotations': {
        'code': "def negation(arg: bool) -> bool:\n    return (not arg)",
        'is_expression': False,
        'tree': typed_ast.ast35.FunctionDef(
            'negation',
            typed_ast.ast35.arguments(
                [typed_ast.ast35.arg('arg', typed_ast.ast35.Name('bool', typed_ast.ast35.Load()))],
                None, [], [], None, []),
            [typed_ast.ast35.Return(typed_ast.ast35.UnaryOp(
                typed_ast.ast35.Not(), typed_ast.ast35.Name('arg', typed_ast.ast35.Load())
                ))],
            [], typed_ast.ast35.Name('bool', typed_ast.ast35.Load()), None
            ),
        'dump': \
            "FunctionDef(name='negation',args=arguments(" \
                "args=[arg(arg='arg',annotation=Name(id='bool',ctx=Load()))]," \
                "vararg=None,kwonlyargs=[],kw_defaults=[],kwarg=None,defaults=[])," \
            "body=[Return(value=UnaryOp(op=Not(),operand=Name(id='arg',ctx=Load())))]," \
            "decorator_list=[],returns=Name(id='bool',ctx=Load()),type_comment=None)"
        }
    }

def generate_variants(example: dict):
    if example['is_expression']:
        example['trees'] = {
            'exec': typed_ast.ast35.Module([typed_ast.ast35.Expr(example['tree'])], []),
            'eval': typed_ast.ast35.Expression(example['tree']),
            'single': typed_ast.ast35.Interactive([typed_ast.ast35.Expr(example['tree'])])
            }
        example['dumps'] = {
            'exec': 'Module(body=[Expr(value={})],type_ignores=[])'.format(example['dump']),
            'eval': 'Expression(body={})'.format(example['dump']),
            'single': 'Interactive(body=[Expr(value={})])'.format(example['dump'])
            }
    else:
        example['trees'] = {
            'exec': typed_ast.ast35.Module([example['tree']], []),
            'eval': None,
            'single': typed_ast.ast35.Interactive([example['tree']])
            }
        example['dumps'] = {
            'exec': 'Module(body=[{}],type_ignores=[])'.format(example['dump']),
            'eval': None,
            'single': 'Interactive(body=[{}])'.format(example['dump'])
            }

for _, example in EXAMPLES.items():
    generate_variants(example)

# verify examples
if __debug__:
    _MSG = '''example for {} in '{}' mode is incorrect:
"""
{}
"""
tree from source (above) != example tree (below)
"""
{}
"""'''
    for description, example in EXAMPLES.items():
        for mode in MODES:
            if example['trees'][mode] is None:
                try:
                    tree_from_source = typed_ast.ast35.parse(
                        source=example['code'], filename='<string>', mode=mode)
                except SyntaxError:
                    tree_from_source = None
                example_tree = None
            else:
                tree_from_source = typed_astunparse.dump(
                    typed_ast.ast35.parse(source=example['code'], filename='<string>', mode=mode)
                    ).replace('\n', '').replace(' ', '')
                example_tree = typed_astunparse.dump(
                    example['trees'][mode]).replace('\n', '').replace(' ', '')
            assert tree_from_source == example_tree, _MSG.format(
                description, mode, tree_from_source, example_tree)
